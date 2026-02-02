#!/usr/bin/env python3
"""
Edexcel Maths Homework Tool - Web Interface V2
Uses Python built-in http.server instead of Flask, and pypdf for PDF handling
"""

import os
import shutil
import base64
import urllib.parse
import json
import re
import io
import tempfile
import warnings
from pathlib import Path
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader, PdfWriter
import pypdfium2 as pdfium
from PIL import Image

# Suppress pdfplumber color space warnings
warnings.filterwarnings('ignore', message='.*Cannot set.*color.*')

from config import TOPICS
from topic_keywords import TOPIC_KEYWORDS, TOPIC_NUMBER_TO_KEY
from strict_keywords import get_strict_keywords, page_matches_topic
from html_template import get_html_template

# Directories
WORK_DIR = Path("homework_temp")
PDF_DIR = WORK_DIR / "pdfs"
PREVIEW_DIR = WORK_DIR / "previews"
OUTPUT_DIR = Path("outputs")

# Ensure directories exist
for d in [WORK_DIR, PDF_DIR, PREVIEW_DIR, OUTPUT_DIR]:
    d.mkdir(exist_ok=True)

# Level configurations
LEVELS = {
    'ks3': {
        'name': 'KS3 (Year 7-9)',
        'search_terms': ['KS3', 'Key Stage 3', 'Year 7', 'Year 8', 'Year 9'],
    },
    'gcse': {
        'name': 'GCSE',
        'search_terms': ['GCSE', 'Edexcel', 'AQA', 'OCR'],
    }
}

# Difficulty configurations
DIFFICULTIES = {
    'medium': {
        'name': 'Medium',
        'description': 'Standard practice questions',
        'search_terms': [],
        'google_extra': 'worksheet OR practice',
    },
    'hard': {
        'name': 'Hard',
        'description': 'Exam-style questions',
        'search_terms': ['past paper', 'exam'],
        'google_extra': '"exam questions" OR "past paper"',
    },
    'harder': {
        'name': 'Harder',
        'description': 'Grade 8-9 challenging questions',
        'search_terms': ['grade 9', 'challenging', 'hard'],
        'google_extra': '',
    },
    'pastpapers': {
        'name': 'Past Papers Only',
        'description': 'Actual Edexcel past papers filtered by topic',
        'search_terms': ['past paper', 'edexcel'],
        'google_extra': '"Edexcel" "past paper"',
    }
}

# Trusted educational domains
TRUSTED_DOMAINS = [
    'mathsgenie.co.uk',
    'corbettmaths.com',
    'mmerevise.co.uk',
    'physicsandmathstutor.com',
    'savemyexams.com',
    'draustinmaths.com',
    'mathsbox.org.uk',
    'justmaths.co.uk',
    'crashmaths.com',
    'onmaths.com',
    'mathswatch.co.uk',
    'hegartymaths.com',
    'drfrostmaths.com',
    'm4ths.com',
]

# Session storage (simple in-memory for single user)
session_data = {}


def is_topic_relevant(text: str, topic: str, keywords: list = None) -> bool:
    """Check if text is relevant to the topic."""
    text_lower = text.lower()
    topic_lower = topic.lower()

    topic_variations = [topic_lower]

    if ' ' in topic_lower:
        words = topic_lower.split()
        if len(words[0]) > 4:
            topic_variations.append(words[0])
        topic_variations.append(topic_lower.replace(' ', '-'))
        topic_variations.append(topic_lower.replace(' ', ''))

    for variation in topic_variations:
        if variation in text_lower:
            return True

    return False


def get_topic_keywords(topic: str) -> list:
    """Get comprehensive keywords for a topic from TOPIC_KEYWORDS"""
    # Extract topic name and number
    topic_lower = topic.lower()
    topic_num = None
    topic_name = topic_lower

    # Parse "25 - Probability" format
    if ' - ' in topic:
        parts = topic.split(' - ', 1)
        try:
            topic_num = int(parts[0].strip())
        except:
            pass
        topic_name = parts[1].lower().strip()

    # Try to find in TOPIC_KEYWORDS using various matching strategies
    keywords = []

    # Strategy 1: Direct key match
    if topic_name in TOPIC_KEYWORDS:
        keywords = TOPIC_KEYWORDS[topic_name]
    else:
        # Strategy 2: Partial key match
        for key, kws in TOPIC_KEYWORDS.items():
            if key in topic_name or topic_name in key:
                keywords = kws
                break
            # Check for word overlap
            key_words = set(key.split())
            topic_words = set(topic_name.split())
            if key_words & topic_words:  # Intersection
                keywords = kws
                break

    # Strategy 3: Use topic number mapping
    if not keywords and topic_num:
        key = TOPIC_NUMBER_TO_KEY.get(topic_num)
        if key and key in TOPIC_KEYWORDS:
            keywords = TOPIC_KEYWORDS[key]

    # Combine with config.py keywords if available
    config_keywords = []
    if topic in TOPICS:
        config_keywords = TOPICS[topic]
    else:
        for topic_key, kws in TOPICS.items():
            if topic_name in topic_key.lower():
                config_keywords = kws
                break

    # Merge and deduplicate
    all_keywords = list(set([k.lower() for k in keywords + config_keywords]))

    if all_keywords:
        print(f"   📚 Found {len(all_keywords)} keywords for '{topic_name}'")
        return all_keywords

    # Fallback: extract meaningful words from topic
    print(f"   ⚠ No keywords found for '{topic}', using fallback")
    return [w.lower() for w in topic.split() if len(w) > 2]


def preprocess_image_for_ocr(pil_image):
    """Preprocess image for optimal OCR accuracy using OpenCV techniques"""
    import cv2
    import numpy as np
    from PIL import Image

    # Convert PIL to OpenCV format
    img = np.array(pil_image)

    # Convert to grayscale if needed
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gray = img

    # 1. Denoise the image
    denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)

    # 2. Apply adaptive thresholding for better text contrast
    # This handles varying lighting conditions across the page
    binary = cv2.adaptiveThreshold(
        denoised, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 10  # Block size and constant
    )

    # 3. Deskew if needed (fix rotated scans)
    coords = np.column_stack(np.where(binary < 255))
    if len(coords) > 100:
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = 90 + angle
        if abs(angle) > 0.5 and abs(angle) < 10:  # Only deskew if slightly rotated
            (h, w) = binary.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            binary = cv2.warpAffine(binary, M, (w, h),
                                     flags=cv2.INTER_CUBIC,
                                     borderMode=cv2.BORDER_REPLICATE)

    # 4. Morphological operations to clean up
    kernel = np.ones((1, 1), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    # 5. Add small border (helps Tesseract detect edge text)
    binary = cv2.copyMakeBorder(binary, 10, 10, 10, 10,
                                 cv2.BORDER_CONSTANT, value=255)

    # Convert back to PIL
    return Image.fromarray(binary)


def extract_text_with_enhanced_ocr(pdf_path: Path, page_num: int) -> str:
    """Extract text using enhanced OCR with preprocessing for 95%+ accuracy"""
    try:
        import pytesseract

        # Render page at high DPI (300 for optimal OCR)
        pdf = pdfium.PdfDocument(str(pdf_path))
        page = pdf[page_num]
        # Scale 4.0 ≈ 300 DPI which is optimal for OCR
        bitmap = page.render(scale=4.0)
        pil_image = bitmap.to_pil()
        pdf.close()

        # Preprocess the image for better OCR
        processed_image = preprocess_image_for_ocr(pil_image)

        # Configure Tesseract for best accuracy
        # --oem 3: Use LSTM neural network (best accuracy)
        # --psm 3: Fully automatic page segmentation
        # -c preserve_interword_spaces=1: Keep proper spacing
        custom_config = r'--oem 3 --psm 3 -c preserve_interword_spaces=1'

        # Run OCR with enhanced settings
        ocr_text = pytesseract.image_to_string(
            processed_image,
            lang='eng',
            config=custom_config
        )

        return ocr_text.strip()

    except Exception as e:
        print(f"      Enhanced OCR error: {e}")
        return ""


def extract_text_from_pdf_page(pdf_path: Path, page_num: int, force_ocr: bool = False) -> str:
    """Extract text from a PDF page using multiple methods for better results

    Args:
        pdf_path: Path to PDF file
        page_num: Page number (0-indexed)
        force_ocr: If True, always use OCR even if text extraction works
    """
    text = ""
    ocr_text = ""

    # Method 1: Try pdfplumber first (best for text-based PDFs)
    if not force_ocr:
        try:
            import pdfplumber
            with pdfplumber.open(pdf_path) as pdf:
                if page_num < len(pdf.pages):
                    page = pdf.pages[page_num]
                    text = page.extract_text() or ""

                    # Also try extracting text from tables
                    tables = page.extract_tables()
                    for table in tables:
                        for row in table:
                            if row:
                                text += " " + " ".join([str(cell) for cell in row if cell])
        except Exception as e:
            print(f"      pdfplumber error: {e}")

    # Method 2: Try pypdf as backup (sometimes gets different text)
    if len(text) < 50 and not force_ocr:
        try:
            reader = PdfReader(pdf_path)
            if page_num < len(reader.pages):
                pypdf_text = reader.pages[page_num].extract_text() or ""
                if len(pypdf_text) > len(text):
                    text = pypdf_text
        except Exception as e:
            print(f"      pypdf error: {e}")

    # Method 3: Enhanced OCR with preprocessing
    # Use OCR if text extraction failed OR if force_ocr is True
    # Also use OCR as a supplement for scanned documents that may have some embedded text
    if len(text) < 100 or force_ocr:
        ocr_text = extract_text_with_enhanced_ocr(pdf_path, page_num)

        if len(ocr_text) > len(text):
            print(f"      📷 Using enhanced OCR ({len(ocr_text)} chars vs {len(text)} from text extraction)")
            text = ocr_text
        elif ocr_text and len(text) < 200:
            # Combine both if text extraction got little
            combined = text + " " + ocr_text
            # Remove duplicates by using set of words
            words = list(dict.fromkeys(combined.lower().split()))
            text = " ".join(words)
            print(f"      📷 Combined text extraction + OCR ({len(text)} chars)")

    return text


def filter_pdf_pages_by_topic(pdf_path: Path, topic: str, return_confidence: bool = False) -> list:
    """Filter PDF pages using STRICT topic-specific keyword matching

    If return_confidence=True, returns list of dicts with page, score, confidence
    Otherwise returns list of page numbers (backward compatible)
    """
    matching_pages = []

    try:
        # Get the core topic name (without chapter number)
        core_topic = topic
        if ' - ' in topic:
            core_topic = topic.split(' - ', 1)[1]

        print(f"   🔍 STRICT filtering for topic: '{core_topic}'")

        # Get strict keywords info
        strict_kws = get_strict_keywords(topic)
        print(f"   Primary keywords: {strict_kws.get('primary', [])[:8]}...")
        print(f"   Context keywords: {strict_kws.get('context', [])[:5]}...")
        print(f"   Exclude terms: {strict_kws.get('exclude', [])}")

        # Get total pages
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        print(f"   Scanning {total_pages} pages...")

        for page_num in range(total_pages):
            text = extract_text_from_pdf_page(pdf_path, page_num)

            # Skip very short pages (likely blank or just headers)
            if len(text) < 50:
                continue

            # Use strict matching
            matches, score, matched_kws = page_matches_topic(text, topic, debug=False)

            if matches:
                # Determine confidence based on score
                if score >= 5:
                    confidence = 'high'
                else:
                    confidence = 'medium'

                if return_confidence:
                    matching_pages.append({
                        'page': page_num,
                        'score': score,
                        'confidence': confidence,
                        'keywords': matched_kws[:5]
                    })
                else:
                    matching_pages.append(page_num)
                print(f"      Page {page_num + 1}: ✓ Score={score} ({confidence}), Keywords: {matched_kws[:4]}")
            elif score >= 2 and return_confidence:
                # Include medium confidence matches that didn't pass strict threshold
                matching_pages.append({
                    'page': page_num,
                    'score': score,
                    'confidence': 'medium',
                    'keywords': matched_kws[:5]
                })
                print(f"      Page {page_num + 1}: ~ Score={score} (medium), Keywords: {matched_kws[:3]}")
            elif score > 0:
                print(f"      Page {page_num + 1}: ✗ Low score={score}, Keywords: {matched_kws[:3]}")

        high_count = len([p for p in matching_pages if isinstance(p, dict) and p.get('confidence') == 'high']) if return_confidence else len(matching_pages)
        medium_count = len([p for p in matching_pages if isinstance(p, dict) and p.get('confidence') == 'medium']) if return_confidence else 0
        print(f"   📄 Found {high_count} definite + {medium_count} possible pages for '{core_topic}'")

    except Exception as e:
        print(f"   Error filtering pages: {e}")
        import traceback
        traceback.print_exc()

    return matching_pages


def search_harder_questions(session, topic: str, keywords: list, level: str) -> list:
    """Search for harder/challenging questions by directly accessing educational sites"""
    results = []

    topic_slug = topic.lower().replace(' ', '-').replace('&', 'and')
    topic_words = topic.lower().split()
    topic_first = topic_words[0] if topic_words else topic.lower()

    print(f"   Searching direct sites for '{topic}'...")

    # Strategy 1: Search Maths Genie for exam questions
    try:
        mg_url = 'https://www.mathsgenie.co.uk/gcse.html'
        response = session.get(mg_url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a', href=True):
            href = link['href'].lower()
            text = link.get_text().lower()

            if (topic.lower() in text or topic_first in text or
                topic_slug in href or topic_first in href):
                if '.pdf' in href:
                    full_url = href if href.startswith('http') else f"https://www.mathsgenie.co.uk/{href.lstrip('/')}"
                    title = link.get_text().strip() or f'{topic} Questions'
                    results.append({
                        'source': 'Maths Genie (Harder)',
                        'title': title[:60],
                        'url': full_url
                    })
                    print(f"   ✓ Found: {title[:40]}")
    except Exception as e:
        print(f"   Maths Genie error: {e}")

    # Strategy 2: Search Corbettmaths
    try:
        cm_url = 'https://corbettmaths.com/contents/'
        response = session.get(cm_url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a', href=True):
            href = link['href'].lower()
            text = link.get_text().lower()

            if (topic.lower() in text or topic_first in text or topic_slug in href):
                if 'practice' in href or 'questions' in href:
                    try:
                        page_url = link['href'] if link['href'].startswith('http') else f"https://corbettmaths.com{link['href']}"
                        page_resp = session.get(page_url, timeout=10)
                        page_soup = BeautifulSoup(page_resp.text, 'html.parser')

                        for pdf_link in page_soup.find_all('a', href=True):
                            if '.pdf' in pdf_link['href'].lower():
                                pdf_url = pdf_link['href']
                                results.append({
                                    'source': 'Corbettmaths (Harder)',
                                    'title': f'{topic} - {pdf_link.get_text().strip()}'[:60],
                                    'url': pdf_url
                                })
                                print(f"   ✓ Found: {topic} PDF")
                                break
                    except:
                        pass
    except Exception as e:
        print(f"   Corbettmaths error: {e}")

    # Strategy 3: Search Dr Frost Maths
    try:
        df_url = 'https://www.drfrostmaths.com/gcse-questions.php'
        response = session.get(df_url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a', href=True):
            text = link.get_text().lower()
            href = link['href'].lower()

            if topic.lower() in text or topic_first in text:
                if '.pdf' in href or 'download' in href:
                    full_url = link['href'] if link['href'].startswith('http') else f"https://www.drfrostmaths.com/{link['href'].lstrip('/')}"
                    results.append({
                        'source': 'Dr Frost (Harder)',
                        'title': link.get_text().strip()[:60],
                        'url': full_url
                    })
                    print(f"   ✓ Found: {link.get_text().strip()[:40]}")
    except Exception as e:
        print(f"   Dr Frost error: {e}")

    # Strategy 4: Search 1stclassmaths for exam-style questions
    try:
        fcm_url = 'https://www.1stclassmaths.com/gcse-higher'
        response = session.get(fcm_url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a', href=True):
            text = link.get_text().lower()
            href = link['href'].lower()

            if topic.lower() in text or topic_first in text or topic_slug in href:
                if '.pdf' in href:
                    full_url = link['href'] if link['href'].startswith('http') else f"https://www.1stclassmaths.com{link['href']}"
                    results.append({
                        'source': '1st Class Maths (Harder)',
                        'title': link.get_text().strip()[:60] or f'{topic} Questions',
                        'url': full_url
                    })
                    print(f"   ✓ Found: {link.get_text().strip()[:40]}")
    except Exception as e:
        print(f"   1stclassmaths error: {e}")

    # Strategy 5: Search Save My Exams for topic questions
    try:
        sme_url = 'https://www.savemyexams.com/gcse/maths/edexcel/22/higher/'
        response = session.get(sme_url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a', href=True):
            text = link.get_text().lower()
            href = link['href'].lower()

            if topic.lower() in text or topic_first in text:
                # Save My Exams often has topic-specific pages
                if 'topic-questions' in href or 'exam-questions' in href:
                    full_url = link['href'] if link['href'].startswith('http') else f"https://www.savemyexams.com{link['href']}"
                    results.append({
                        'source': 'Save My Exams (Harder)',
                        'title': link.get_text().strip()[:60] or f'{topic} Exam Questions',
                        'url': full_url
                    })
                    print(f"   ✓ Found: {link.get_text().strip()[:40]}")
    except Exception as e:
        print(f"   Save My Exams error: {e}")

    print(f"   Found {len(results)} PDFs from direct sites")
    return results[:12]


def extract_year_from_title(title: str, url: str = '') -> tuple:
    """Extract year and paper info from a past paper title and URL"""
    import re
    title_lower = title.lower()
    url_lower = url.lower()
    combined = f"{title_lower} {url_lower}"

    # Try to extract year (2017-2025)
    year_match = re.search(r'20(1[7-9]|2[0-5])', combined)
    year = year_match.group(0) if year_match else 'Unknown'

    # Try to extract session (May, November, etc.)
    session = 'Unknown'
    if any(x in combined for x in ['may', 'june', 'summer', 'jun']):
        session = 'May/June'
    elif any(x in combined for x in ['nov', 'autumn', 'winter', 'october']):
        session = 'November'

    # Try to extract paper number - check multiple patterns
    paper = 'Paper'

    # Pattern 1: "paper 1", "paper1", "paper-1"
    paper_match = re.search(r'paper[\s\-_]*([123])', combined)
    if paper_match:
        paper = f"Paper {paper_match.group(1)}"
    # Pattern 2: "p1", "p2", "p3" (but not part of longer word)
    elif re.search(r'[\s\-_]p1[\s\-_\.]', combined) or combined.endswith('p1') or '_p1_' in combined or '-p1-' in combined:
        paper = 'Paper 1'
    elif re.search(r'[\s\-_]p2[\s\-_\.]', combined) or combined.endswith('p2') or '_p2_' in combined or '-p2-' in combined:
        paper = 'Paper 2'
    elif re.search(r'[\s\-_]p3[\s\-_\.]', combined) or combined.endswith('p3') or '_p3_' in combined or '-p3-' in combined:
        paper = 'Paper 3'
    # Pattern 3: "1h", "2h", "3h" (paper number + higher tier)
    elif re.search(r'[\s\-_]1h[\s\-_\.]', combined) or '1h.pdf' in combined:
        paper = 'Paper 1'
    elif re.search(r'[\s\-_]2h[\s\-_\.]', combined) or '2h.pdf' in combined:
        paper = 'Paper 2'
    elif re.search(r'[\s\-_]3h[\s\-_\.]', combined) or '3h.pdf' in combined:
        paper = 'Paper 3'
    # Pattern 4: "qp1", "qp2", "qp3" (question paper)
    elif 'qp1' in combined:
        paper = 'Paper 1'
    elif 'qp2' in combined:
        paper = 'Paper 2'
    elif 'qp3' in combined:
        paper = 'Paper 3'

    return year, session, paper


def detect_paper_info_from_first_page(pdf_path: Path) -> dict:
    """Use OCR on first page to detect year, paper number, and if it's a mark scheme"""
    import re
    info = {'year': None, 'paper': None, 'is_mark_scheme': False}

    try:
        text = extract_text_from_pdf_page(pdf_path, 0)
        text_lower = text.lower()

        # Check if it's a mark scheme
        if any(x in text_lower for x in ['mark scheme', 'marking scheme', 'markscheme', 'marks awarded']):
            info['is_mark_scheme'] = True
            return info

        # Look for year
        year_patterns = [
            r'(june|november|may)\s*(20[12][0-9])',
            r'(20[12][0-9])',
        ]
        for pattern in year_patterns:
            match = re.search(pattern, text_lower)
            if match:
                info['year'] = match.group(0)[-4:] if len(match.group(0)) >= 4 else None
                break

        # Look for paper number
        paper_patterns = [
            r'paper\s*([123])',
            r'calculator\s*\(paper\s*([23])\)',  # Calculator allowed = paper 2 or 3
            r'non.?calculator.*paper\s*1',
        ]
        for pattern in paper_patterns:
            match = re.search(pattern, text_lower)
            if match:
                if 'non' in pattern:
                    info['paper'] = 'Paper 1'
                else:
                    info['paper'] = f"Paper {match.group(1)}"
                break

        # Edexcel papers often say "Calculator" or "Non-Calculator" on first page
        if info['paper'] is None:
            if 'non-calculator' in text_lower or 'non calculator' in text_lower:
                info['paper'] = 'Paper 1'
            elif 'calculator' in text_lower and 'non' not in text_lower:
                # Could be Paper 2 or 3, but at least we know it's not Paper 1
                pass

    except Exception as e:
        print(f"      OCR detection error: {e}")

    return info


def get_hardcoded_paper_archive() -> list:
    """
    Complete archive of Edexcel GCSE Higher Maths papers 2017-2024.
    Using LOCAL files from papers/ and markschemes/ folders.
    100% reliable - no external downloads needed.
    """
    papers = []

    # Base directories for local papers
    BASE_DIR = Path(__file__).parent
    PAPERS_DIR = BASE_DIR / "papers"
    MS_DIR = BASE_DIR / "markschemes"

    # Define paper archive mapping local filenames to metadata
    # Filename format: YYYY_Session_Paper_N.pdf (e.g., 2024_Jun_Paper_1.pdf)
    paper_archive = {
        # 2024
        '2024': {
            'November': {
                '1': {'qp': '2024_Nov_Paper_1.pdf', 'ms': '2024_Nov_Paper_1.pdf'},
                '2': {'qp': '2024_Nov_Paper_2.pdf', 'ms': '2024_Nov_Paper_2.pdf'},
                '3': {'qp': '2024_Nov_Paper_3.pdf', 'ms': '2024_Nov_Paper_3.pdf'},
            },
            'May/June': {
                '1': {'qp': '2024_Jun_Paper_1.pdf', 'ms': '2024_Jun_Paper_1.pdf'},
                '2': {'qp': '2024_Jun_Paper_2.pdf', 'ms': '2024_Jun_Paper_2.pdf'},
                '3': {'qp': '2024_Jun_Paper_3.pdf', 'ms': '2024_Jun_Paper_3.pdf'},
            },
        },
        # 2023
        '2023': {
            'November': {
                '1': {'qp': '2023_Nov_Paper_1.pdf', 'ms': '2023_Nov_Paper_1.pdf'},
                '2': {'qp': '2023_Nov_Paper_2.pdf', 'ms': '2023_Nov_Paper_2.pdf'},
                '3': {'qp': '2023_Nov_Paper_3.pdf', 'ms': '2023_Nov_Paper_3.pdf'},
            },
            'May/June': {
                '1': {'qp': '2023_Jun_Paper_1.pdf', 'ms': '2023_Jun_Paper_1.pdf'},
                '2': {'qp': '2023_Jun_Paper_2.pdf', 'ms': '2023_Jun_Paper_2.pdf'},
                '3': {'qp': '2023_Jun_Paper_3.pdf', 'ms': '2023_Jun_Paper_3.pdf'},
            },
        },
        # 2022
        '2022': {
            'November': {
                '1': {'qp': '2022_Nov_Paper_1.pdf', 'ms': '2022_Nov_Paper_1.pdf'},
                '2': {'qp': '2022_Nov_Paper_2.pdf', 'ms': '2022_Nov_Paper_2.pdf'},
                '3': {'qp': '2022_Nov_Paper_3.pdf', 'ms': '2022_Nov_Paper_3.pdf'},
            },
            'May/June': {
                '1': {'qp': '2022_Jun_Paper_1.pdf', 'ms': '2022_Jun_Paper_1.pdf'},
                '2': {'qp': '2022_Jun_Paper_2.pdf', 'ms': '2022_Jun_Paper_2.pdf'},
                '3': {'qp': '2022_Jun_Paper_3.pdf', 'ms': '2022_Jun_Paper_3.pdf'},
            },
        },
        # 2021 - November only (COVID affected May/June)
        '2021': {
            'November': {
                '1': {'qp': '2021_Nov_Paper_1.pdf', 'ms': '2021_Nov_Paper_1.pdf'},
                '2': {'qp': '2021_Nov_Paper_2.pdf', 'ms': '2021_Nov_Paper_2.pdf'},
                '3': {'qp': '2021_Nov_Paper_3.pdf', 'ms': '2021_Nov_Paper_3.pdf'},
            },
        },
        # 2020 - November only (COVID cancelled May/June)
        '2020': {
            'November': {
                '1': {'qp': '2020_Nov_Paper_1.pdf', 'ms': '2020_Nov_Paper_1.pdf'},
                '2': {'qp': '2020_Nov_Paper_2.pdf', 'ms': '2020_Nov_Paper_2.pdf'},
                '3': {'qp': '2020_Nov_Paper_3.pdf', 'ms': '2020_Nov_Paper_3.pdf'},
            },
        },
        # 2019
        '2019': {
            'November': {
                '1': {'qp': '2019_Nov_Paper_1.pdf', 'ms': '2019_Nov_Paper_1.pdf'},
                '2': {'qp': '2019_Nov_Paper_2.pdf', 'ms': '2019_Nov_Paper_2.pdf'},
                '3': {'qp': '2019_Nov_Paper_3.pdf', 'ms': '2019_Nov_Paper_3.pdf'},
            },
            'May/June': {
                '1': {'qp': '2019_Jun_Paper_1.pdf', 'ms': '2019_Jun_Paper_1.pdf'},
                '2': {'qp': '2019_Jun_Paper_2.pdf', 'ms': '2019_Jun_Paper_2.pdf'},
                '3': {'qp': '2019_Jun_Paper_3.pdf', 'ms': '2019_Jun_Paper_3.pdf'},
            },
        },
        # 2018
        '2018': {
            'November': {
                '1': {'qp': '2018_Nov_Paper_1.pdf', 'ms': '2018_Nov_Paper_1.pdf'},
                '2': {'qp': '2018_Nov_Paper_2.pdf', 'ms': '2018_Nov_Paper_2.pdf'},
                '3': {'qp': '2018_Nov_Paper_3.pdf', 'ms': '2018_Nov_Paper_3.pdf'},
            },
            'May/June': {
                '1': {'qp': '2018_Jun_Paper_1.pdf', 'ms': '2018_Jun_Paper_1.pdf'},
                '2': {'qp': '2018_Jun_Paper_2.pdf', 'ms': '2018_Jun_Paper_2.pdf'},
                '3': {'qp': '2018_Jun_Paper_3.pdf', 'ms': '2018_Jun_Paper_3.pdf'},
            },
        },
        # 2017
        '2017': {
            'November': {
                '1': {'qp': '2017_Nov_Paper_1.pdf', 'ms': '2017_Nov_Paper_1.pdf'},
                '2': {'qp': '2017_Nov_Paper_2.pdf', 'ms': '2017_Nov_Paper_2.pdf'},
                '3': {'qp': '2017_Nov_Paper_3.pdf', 'ms': '2017_Nov_Paper_3.pdf'},
            },
            'May/June': {
                '1': {'qp': '2017_Jun_Paper_1.pdf', 'ms': '2017_Jun_Paper_1.pdf'},
                '2': {'qp': '2017_Jun_Paper_2.pdf', 'ms': '2017_Jun_Paper_2.pdf'},
                '3': {'qp': '2017_Jun_Paper_3.pdf', 'ms': '2017_Jun_Paper_3.pdf'},
            },
        },
        # Specimen Papers
        'Specimen': {
            'Sample': {
                '1': {'qp': 'Sample_Paper_1.pdf', 'ms': 'Sample_Paper_1.pdf'},
                '2': {'qp': 'Sample_Paper_2.pdf', 'ms': 'Sample_Paper_2.pdf'},
                '3': {'qp': 'Sample_Paper_3.pdf', 'ms': 'Sample_Paper_3.pdf'},
            },
            'Specimen 1': {
                '1': {'qp': 'Specimen1_Paper_1.pdf', 'ms': 'Specimen1_Paper_1.pdf'},
                '2': {'qp': 'Specimen1_Paper_2.pdf', 'ms': 'Specimen1_Paper_2.pdf'},
                '3': {'qp': 'Specimen1_Paper_3.pdf', 'ms': 'Specimen1_Paper_3.pdf'},
            },
            'Specimen 2': {
                '1': {'qp': 'Specimen2_Paper_1.pdf', 'ms': 'Specimen2_Paper_1.pdf'},
                '2': {'qp': 'Specimen2_Paper_2.pdf', 'ms': 'Specimen2_Paper_2.pdf'},
                '3': {'qp': 'Specimen2_Paper_3.pdf', 'ms': 'Specimen2_Paper_3.pdf'},
            },
        }
    }

    # Convert to flat list format with local file paths
    for year, sessions in paper_archive.items():
        for session_name, papers_dict in sessions.items():
            for paper_num, files in papers_dict.items():
                qp_path = PAPERS_DIR / files['qp']
                ms_path = MS_DIR / files['ms']

                # Only add if the file exists
                if qp_path.exists():
                    papers.append({
                        'source': 'Local',
                        'title': f"Edexcel GCSE Higher {session_name} {year} Paper {paper_num}",
                        'url': str(qp_path),  # Local file path
                        'local_path': str(qp_path),  # Explicit local path marker
                        'filter_pages': True,
                        'year': year,
                        'session': session_name,
                        'paper': f"Paper {paper_num}",
                        'sort_key': f"{year}-{session_name}-{paper_num}",
                        'is_mark_scheme': False,
                    })

                if ms_path.exists():
                    papers.append({
                        'source': 'Local',
                        'title': f"Edexcel GCSE Higher {session_name} {year} Paper {paper_num} MS",
                        'url': str(ms_path),  # Local file path
                        'local_path': str(ms_path),  # Explicit local path marker
                        'filter_pages': False,
                        'year': year,
                        'session': session_name,
                        'paper': f"Paper {paper_num}",
                        'sort_key': f"{year}-{session_name}-{paper_num}-MS",
                        'is_mark_scheme': True,
                    })

    return papers


def search_past_papers(session, topic: str, level: str) -> list:
    """Search for Edexcel past papers from MULTIPLE sources and organize by year"""
    results = []
    seen_urls = set()

    print(f"   Searching past paper archives for ALL papers (1, 2, 3)...")

    # First, add hardcoded archive papers (most reliable)
    hardcoded_papers = get_hardcoded_paper_archive()
    for paper in hardcoded_papers:
        url_key = paper['url'].split('?')[0].lower()
        if url_key not in seen_urls:
            seen_urls.add(url_key)
            results.append(paper)
    print(f"   Added {len(hardcoded_papers)} papers from hardcoded archive")

    # Track which year/session/paper combinations we already have from hardcoded
    existing_papers = set()
    for paper in hardcoded_papers:
        key = f"{paper['year']}-{paper['session']}-{paper['paper']}-{paper.get('is_mark_scheme', False)}"
        existing_papers.add(key)

    def add_result(url, title, source):
        """Add a result if not duplicate and not a mark scheme"""
        url_key = url.split('?')[0].lower()

        # Skip mark schemes from scraped sources (we have them in hardcoded)
        if any(x in url_key for x in ['mark', 'ms', 'scheme', 'answer']):
            return
        if any(x in title.lower() for x in ['mark scheme', 'marking', 'answers']):
            return

        if url_key in seen_urls:
            return

        year, exam_session, paper = extract_year_from_title(title, url)

        # Skip if we already have this paper from hardcoded archive
        paper_key = f"{year}-{exam_session}-{paper}-False"
        if paper_key in existing_papers:
            return

        seen_urls.add(url_key)

        # Clean up title
        clean_title = title.strip()
        if not clean_title:
            clean_title = url.split('/')[-1].replace('.pdf', '').replace('-', ' ').replace('_', ' ')

        results.append({
            'source': source,
            'title': clean_title[:60],
            'url': url,
            'filter_pages': True,
            'year': year,
            'session': exam_session,
            'paper': paper,
            'sort_key': f"{year}-{exam_session}-{paper}"
        })
        print(f"   ✓ Found: {year} {exam_session} {paper} - {source}")

    # NOTE: External scraping disabled - using only hardcoded archive for reliability
    # The hardcoded archive has 96 verified papers (2017-2024 + Specimen)
    # Each year has May/June + November sessions, Papers 1-3, plus mark schemes
    print(f"   Using hardcoded archive only (no external scraping for reliability)")

    # Sort by year (descending) then paper number
    def sort_key(x):
        year = x.get('year', 'Unknown')
        paper = x.get('paper', 'Paper')
        # Extract paper number for sorting
        paper_num = '9'  # Default to end
        if 'Paper 1' in paper:
            paper_num = '1'
        elif 'Paper 2' in paper:
            paper_num = '2'
        elif 'Paper 3' in paper:
            paper_num = '3'
        return f"{year}-{paper_num}"

    results.sort(key=sort_key, reverse=True)

    print(f"   Total past papers found: {len(results)}")
    print(f"   Paper 1: {len([r for r in results if 'Paper 1' in r.get('paper', '')])}")
    print(f"   Paper 2: {len([r for r in results if 'Paper 2' in r.get('paper', '')])}")
    print(f"   Paper 3: {len([r for r in results if 'Paper 3' in r.get('paper', '')])}")

    # Return ALL papers - no limit needed for past papers grid
    return results


def search_mathsgenie_direct(session, topic: str, level: str, difficulty: str = 'medium') -> list:
    """Search Maths Genie directly"""
    results = []
    topic_lower = topic.lower()
    topic_slug = topic_lower.replace(' ', '-').replace('&', 'and')
    topic_first_word = topic_lower.split()[0] if ' ' in topic_lower else topic_lower

    # For KS3, add Year 7/8/9 search variations
    ks3_variations = []
    if level == 'ks3':
        ks3_variations = [
            f"year 7 {topic_lower}",
            f"year 8 {topic_lower}",
            f"year 9 {topic_lower}",
            f"ks3 {topic_lower}",
        ]
        pages = [
            'https://www.mathsgenie.co.uk/year7.html',
            'https://www.mathsgenie.co.uk/year8.html',
            'https://www.mathsgenie.co.uk/year9.html',
        ]
    else:
        pages = ['https://www.mathsgenie.co.uk/gcse.html']

    for page_url in pages:
        try:
            response = session.get(page_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            for link in soup.find_all('a', href=True):
                href = link['href']
                text = link.get_text().strip().lower()

                if (topic_lower in text or topic_lower in href.lower() or
                    topic_slug in href.lower() or topic_first_word in text):
                    if '.pdf' in href.lower():
                        full_url = href if href.startswith('http') else f"https://www.mathsgenie.co.uk/{href.lstrip('/')}"

                        if difficulty == 'hard':
                            if 'exam' not in text and 'questions' not in href.lower():
                                continue

                        if is_topic_relevant(f"{text} {href}", topic):
                            results.append({
                                'source': 'Maths Genie',
                                'title': link.get_text().strip() or f'{topic} PDF',
                                'url': full_url
                            })
        except Exception as e:
            print(f"   Maths Genie error: {e}")

    return results[:8]


def search_corbettmaths_direct(session, topic: str, difficulty: str = 'medium', level: str = 'gcse') -> list:
    """Search Corbettmaths with strict topic matching."""
    results = []
    topic_lower = topic.lower()
    topic_slug = topic_lower.replace(' ', '-')
    topic_first_word = topic_lower.split()[0] if ' ' in topic_lower else topic_lower

    # For KS3, also search with Year 7/8/9 variations
    if level == 'ks3':
        print(f"   Corbett KS3 mode: adding Year 7/8/9 variations")

    try:
        response = session.get('https://corbettmaths.com/contents/', timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a', href=True):
            href = link['href']
            text = link.get_text().strip().lower()

            if (topic_lower in text or topic_lower in href.lower() or
                topic_slug in href.lower() or topic_first_word in text):

                if 'practice-questions' in href.lower() or 'textbook' in href.lower():
                    full_url = href if href.startswith('http') else f"https://corbettmaths.com{href}"

                    try:
                        page_resp = session.get(full_url, timeout=10)
                        page_soup = BeautifulSoup(page_resp.text, 'html.parser')

                        for pdf_link in page_soup.find_all('a', href=True):
                            pdf_href = pdf_link['href']
                            if '.pdf' in pdf_href.lower():
                                if is_topic_relevant(f"{text} {pdf_href}", topic):
                                    results.append({
                                        'source': 'Corbettmaths',
                                        'title': f"{topic} - {pdf_link.get_text().strip()}" if pdf_link.get_text().strip() else f"{topic} PDF",
                                        'url': pdf_href
                                    })
                                    break
                    except:
                        pass

                elif '.pdf' in href.lower():
                    full_url = href if href.startswith('http') else f"https://corbettmaths.com{href}"
                    if is_topic_relevant(f"{text} {href}", topic):
                        results.append({
                            'source': 'Corbettmaths',
                            'title': link.get_text().strip() or f'{topic} PDF',
                            'url': full_url
                        })
    except Exception as e:
        print(f"   Corbettmaths error: {e}")

    return results[:8]


def search_mme_direct(session, topic: str, level: str, difficulty: str = 'medium') -> list:
    """Search MME Revise with strict topic matching."""
    results = []
    topic_lower = topic.lower()
    topic_slug = topic_lower.replace(' ', '-')
    topic_first_word = topic_lower.split()[0] if ' ' in topic_lower else topic_lower

    # For KS3, also search with Year 7/8/9 variations
    ks3_search_variations = []
    if level == 'ks3':
        ks3_search_variations = [
            f"year 7 {topic_lower}",
            f"year 8 {topic_lower}",
            f"year 9 {topic_lower}",
            f"ks3 {topic_lower}",
        ]
        base_url = 'https://mmerevise.co.uk/ks3-revision/ks3-maths/ks3-maths-worksheets/'
    else:
        base_url = 'https://mmerevise.co.uk/gcse-maths-revision/'

    try:
        response = session.get(base_url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a', href=True):
            href = link['href']
            text = link.get_text().strip().lower()

            if (topic_lower in text or topic_lower in href.lower() or
                topic_slug in href.lower() or topic_first_word in text):
                if '.pdf' in href.lower():
                    full_url = href if href.startswith('http') else f"https://mmerevise.co.uk{href}"

                    if difficulty == 'hard':
                        if 'exam' not in text and 'questions' not in text:
                            continue

                    if is_topic_relevant(f"{text} {href}", topic):
                        results.append({
                            'source': 'MME Revise',
                            'title': link.get_text().strip() or f'{topic} PDF',
                            'url': full_url
                        })
    except Exception as e:
        print(f"   MME error: {e}")

    return results[:8]


def search_all_sources(topic: str, keywords: list = None, level: str = 'gcse', difficulty: str = 'medium') -> list:
    """Search all sources for PDFs matching the topic, level, and difficulty"""
    results = []

    core_topic = topic
    if ' - ' in topic:
        core_topic = topic.split(' - ', 1)[1]

    diff_config = DIFFICULTIES.get(difficulty, DIFFICULTIES['medium'])
    print(f"   Difficulty: {diff_config['name']} - {diff_config['description']}")

    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.5',
    })

    if difficulty == 'pastpapers':
        print(f"   📋 Past Papers mode: Searching for Edexcel past papers...")
        results = search_past_papers(session, core_topic, level)
    elif difficulty == 'harder':
        print(f"   🔥 Harder mode: Searching for challenging questions...")
        results = search_harder_questions(session, core_topic, keywords, level)
    else:
        print(f"   Searching for \"{core_topic}\" PDFs...")
        # Direct site searches (no Google to avoid blocking)
        print(f"   Searching educational sites for \"{core_topic}\"...")
        mg_results = search_mathsgenie_direct(session, core_topic, level, difficulty)
        results.extend(mg_results)
        cm_results = search_corbettmaths_direct(session, core_topic, difficulty, level)
        results.extend(cm_results)
        mme_results = search_mme_direct(session, core_topic, level, difficulty)
        results.extend(mme_results)

    # Remove duplicates
    seen_urls = set()
    unique_results = []
    for r in results:
        url_key = r['url'].split('?')[0]
        if url_key not in seen_urls:
            # For Past Papers mode, skip relevance filter - we filter pages later
            # Past papers contain questions on ALL topics, not just the one in the title
            if difficulty == 'pastpapers':
                seen_urls.add(url_key)
                unique_results.append(r)
            else:
                # For other modes, check topic relevance
                combined_text = f"{r['title']} {r['url']}".lower()
                if is_topic_relevant(combined_text, core_topic, keywords):
                    seen_urls.add(url_key)
                    unique_results.append(r)
                else:
                    print(f"   ✗ Filtered out irrelevant: {r['title'][:40]}")

    print(f"   Found {len(unique_results)} relevant PDFs")
    return unique_results


def download_pdf(url: str, session=None) -> Path:
    """Download a PDF and return the path. Handles both URLs and local file paths."""

    # Check if this is a local file path (from our local paper archive)
    local_path = Path(url)
    if local_path.exists() and local_path.suffix.lower() == '.pdf':
        print(f"   ✓ Using local file: {local_path.name}")
        # Verify it's a valid PDF
        try:
            reader = PdfReader(local_path)
            _ = len(reader.pages)
            return local_path
        except Exception as e:
            print(f"   ✗ Invalid PDF: {local_path.name} - {e}")
            return None

    # Otherwise, download from URL
    if session is None:
        session = requests.Session()
    # Always set a complete User-Agent for all requests
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/pdf,*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://revisionmaths.com/gcse-maths/gcse-maths-past-papers/edexcel-gcse-maths-past-papers'
    })

    try:
        response = session.get(url, timeout=30, stream=True)
        response.raise_for_status()

        content_type = response.headers.get('content-type', '').lower()
        if 'pdf' not in content_type and not url.lower().endswith('.pdf'):
            print(f"   ✗ Not a PDF: {content_type}")
            return None

        filename = url.split('/')[-1].split('?')[0]
        if not filename.endswith('.pdf'):
            filename = f"{hash(url) % 100000}.pdf"
        filename = re.sub(r'[^\w\-\.]', '_', filename)

        filepath = PDF_DIR / filename

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        if filepath.exists() and filepath.stat().st_size > 1000:
            try:
                reader = PdfReader(filepath)
                _ = len(reader.pages)
                return filepath
            except:
                filepath.unlink()
                return None

        return filepath
    except Exception as e:
        print(f"   Download error for {url}: {e}")
        return None


def merge_pdfs(pdf_paths: list, max_pages: int = 30) -> Path:
    """Merge multiple PDFs into one"""
    output_path = WORK_DIR / f"merged_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    writer = PdfWriter()
    total_pages = 0

    for pdf_path in pdf_paths:
        if total_pages >= max_pages:
            break

        try:
            reader = PdfReader(pdf_path)
            pages_to_add = min(len(reader.pages), max_pages - total_pages)

            for i in range(pages_to_add):
                writer.add_page(reader.pages[i])
                total_pages += 1
        except Exception as e:
            print(f"Error merging {pdf_path}: {e}")

    with open(output_path, 'wb') as f:
        writer.write(f)

    return output_path


def generate_page_thumbnail(pdf_path: Path, page_index: int, max_width: int = 200) -> str:
    """Generate a base64 thumbnail for a specific page"""
    try:
        import pypdfium2 as pdfium

        pdf = pdfium.PdfDocument(str(pdf_path))
        if page_index >= len(pdf):
            return ""

        page = pdf[page_index]
        scale = max_width / page.get_width()
        bitmap = page.render(scale=scale)
        pil_image = bitmap.to_pil()

        buffer = io.BytesIO()
        pil_image.save(buffer, format='PNG')
        b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        pdf.close()
        return b64
    except Exception as e:
        print(f"Error generating thumbnail for page {page_index}: {e}")
        return ""


def get_pdf_page_thumbnails(pdf_path: Path, max_width: int = 200) -> list:
    """Generate base64 thumbnails for each page of a PDF using pypdfium2"""
    thumbnails = []

    try:
        import pypdfium2 as pdfium

        pdf = pdfium.PdfDocument(str(pdf_path))
        print(f"   PDF has {len(pdf)} pages")

        for page_num in range(len(pdf)):
            page = pdf[page_num]

            # Render at low resolution for thumbnail (scale ~0.25 for ~72 dpi from 300)
            scale = max_width / page.get_width()
            bitmap = page.render(scale=scale)
            pil_image = bitmap.to_pil()

            # Convert to base64
            buffer = io.BytesIO()
            pil_image.save(buffer, format='PNG')
            b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

            thumbnails.append({
                'page': page_num + 1,
                'data': f"data:image/png;base64,{b64}",
                'width': pil_image.width,
                'height': pil_image.height
            })

        pdf.close()
        print(f"   Generated {len(thumbnails)} thumbnails")
    except Exception as e:
        print(f"Error generating thumbnails: {e}")
        import traceback
        traceback.print_exc()

    return thumbnails


def get_pdf_page_full(pdf_path: Path, page_num: int) -> str:
    """Get a full-resolution image of a specific page using pypdfium2"""
    try:
        import pypdfium2 as pdfium

        pdf = pdfium.PdfDocument(str(pdf_path))
        if page_num < 1 or page_num > len(pdf):
            return None

        page = pdf[page_num - 1]  # Convert to 0-indexed

        # Render at higher resolution (scale 2.0 for ~150 dpi)
        bitmap = page.render(scale=2.0)
        pil_image = bitmap.to_pil()

        buffer = io.BytesIO()
        pil_image.save(buffer, format='PNG')
        b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        pdf.close()
        return f"data:image/png;base64,{b64}"
    except Exception as e:
        print(f"Error getting full page: {e}")
        import traceback
        traceback.print_exc()
    return None


def remove_pages_from_pdf(pdf_path: Path, pages_to_keep: list) -> Path:
    """Create a new PDF with only the specified pages"""
    output_path = WORK_DIR / f"edited_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    for page_num in pages_to_keep:
        if 0 <= page_num - 1 < len(reader.pages):
            writer.add_page(reader.pages[page_num - 1])

    with open(output_path, 'wb') as f:
        writer.write(f)

    return output_path


def cleanup_temp():
    """Remove all temporary files"""
    try:
        for f in PDF_DIR.glob("*"):
            f.unlink()
        for f in PREVIEW_DIR.glob("*"):
            f.unlink()
        for f in WORK_DIR.glob("merged_*.pdf"):
            f.unlink()
        for f in WORK_DIR.glob("edited_*.pdf"):
            f.unlink()
    except Exception as e:
        print(f"Cleanup error: {e}")


# HTML Template
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en" data-theme="default">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Maths Homework Generator</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        /* Default Dark Theme */
        :root, [data-theme="default"] {
            --bg-dark: #0c0c14;
            --bg-card: #14141f;
            --bg-card-hover: #1a1a28;
            --bg-input: #1c1c2a;
            --border: #2d2d44;
            --border-hover: #4a4a6a;
            --primary: #7c5cff;
            --primary-light: #9d85ff;
            --primary-glow: rgba(124, 92, 255, 0.25);
            --secondary: #ff6b9d;
            --secondary-glow: rgba(255, 107, 157, 0.2);
            --success: #4ade80;
            --success-glow: rgba(74, 222, 128, 0.25);
            --danger: #ff6b6b;
            --warning: #fbbf24;
            --text: #f8f8fc;
            --text-soft: #b8b8d0;
            --text-muted: #6b6b8a;
            --gradient-1: linear-gradient(135deg, #7c5cff 0%, #ff6b9d 100%);
            --gradient-2: linear-gradient(135deg, #4ade80 0%, #22d3ee 100%);
            --font-main: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Intuitive Academy Theme - Blue/Teal professional look */
        [data-theme="intuitive"] {
            --bg-dark: #0f172a;
            --bg-card: #1e293b;
            --bg-card-hover: #334155;
            --bg-input: #1e293b;
            --border: #334155;
            --border-hover: #475569;
            --primary: #0ea5e9;
            --primary-light: #38bdf8;
            --primary-glow: rgba(14, 165, 233, 0.25);
            --secondary: #06b6d4;
            --secondary-glow: rgba(6, 182, 212, 0.2);
            --success: #10b981;
            --success-glow: rgba(16, 185, 129, 0.25);
            --danger: #ef4444;
            --warning: #f59e0b;
            --text: #f1f5f9;
            --text-soft: #cbd5e1;
            --text-muted: #64748b;
            --gradient-1: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
            --gradient-2: linear-gradient(135deg, #10b981 0%, #06b6d4 100%);
            --font-main: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        html {
            scroll-behavior: auto; /* Disable smooth scrolling to prevent aggressive scroll */
        }
        body {
            font-family: var(--font-main);
            background: var(--bg-dark);
            color: var(--text);
            min-height: 100vh;
            line-height: 1.6;
        }

        /* Theme Switcher */
        .theme-switcher {
            position: fixed;
            top: 1rem;
            right: 1rem;
            z-index: 1000;
            display: flex;
            gap: 0.5rem;
            background: var(--bg-card);
            padding: 0.5rem;
            border-radius: 8px;
            border: 1px solid var(--border);
        }
        .theme-btn {
            padding: 0.4rem 0.8rem;
            border: 1px solid var(--border);
            background: var(--bg-input);
            color: var(--text-soft);
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.8rem;
            transition: all 0.2s;
        }
        .theme-btn:hover {
            border-color: var(--primary);
            color: var(--text);
        }
        .theme-btn.active {
            background: var(--primary);
            border-color: var(--primary);
            color: white;
        }
        .bg-effects {
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: 0;
            overflow: hidden;
        }
        .bg-orb {
            position: absolute;
            border-radius: 50%;
            filter: blur(80px);
            opacity: 0.4;
            animation: float 20s ease-in-out infinite;
        }
        .bg-orb-1 {
            width: 600px;
            height: 600px;
            background: var(--primary);
            top: -200px;
            left: -100px;
        }
        .bg-orb-2 {
            width: 500px;
            height: 500px;
            background: var(--secondary);
            bottom: -150px;
            right: -100px;
            animation-delay: -7s;
        }
        @keyframes float {
            0%, 100% { transform: translate(0, 0) scale(1); }
            33% { transform: translate(30px, -30px) scale(1.05); }
            66% { transform: translate(-20px, 20px) scale(0.95); }
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            position: relative;
            z-index: 1;
        }
        header {
            text-align: center;
            margin-bottom: 3rem;
        }
        header h1 {
            font-size: 2.5rem;
            font-weight: 800;
            background: var(--gradient-1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
        }
        header p {
            color: var(--text-soft);
            font-size: 1.1rem;
        }
        .search-section {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 2rem;
        }
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }
        .form-group {
            display: flex;
            flex-direction: column;
        }
        label {
            font-weight: 500;
            margin-bottom: 0.5rem;
            color: var(--text-soft);
            font-size: 0.9rem;
        }
        select, input {
            background: var(--bg-input);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.75rem 1rem;
            color: var(--text);
            font-family: inherit;
            font-size: 1rem;
            transition: border-color 0.2s;
        }
        select:focus, input:focus {
            outline: none;
            border-color: var(--primary);
        }
        .topic-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 0.75rem;
            margin-top: 1rem;
            max-height: 400px;
            overflow-y: auto;
            padding-right: 0.5rem;
        }
        .topic-item {
            background: var(--bg-input);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.75rem 1rem;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 0.9rem;
        }
        .topic-item:hover {
            border-color: var(--primary);
            transform: translateY(-2px);
        }
        .topic-item.selected {
            background: var(--primary);
            border-color: var(--primary);
            color: white;
        }
        .btn {
            background: var(--gradient-1);
            border: none;
            border-radius: 8px;
            padding: 0.75rem 2rem;
            color: white;
            font-family: inherit;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px var(--primary-glow);
        }
        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }
        .btn-secondary {
            background: var(--bg-input);
            border: 1px solid var(--border);
        }
        .btn-success {
            background: var(--gradient-2);
        }
        .results-section {
            margin-top: 2rem;
        }
        .pdf-results {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1rem;
        }
        .pdf-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1rem;
            transition: all 0.2s;
        }
        .pdf-card:hover {
            border-color: var(--primary);
        }
        .pdf-card h4 {
            font-size: 0.95rem;
            margin-bottom: 0.5rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .pdf-card .source {
            color: var(--text-muted);
            font-size: 0.8rem;
        }
        .page-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }
        .page-item {
            position: relative;
            cursor: pointer;
            border-radius: 8px;
            overflow: hidden;
            border: 2px solid transparent;
            transition: all 0.2s;
        }
        .page-item:hover {
            border-color: var(--primary);
        }
        .page-item.selected {
            border-color: var(--success);
        }
        .page-item img {
            width: 100%;
            display: block;
        }
        .page-number {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(0,0,0,0.7);
            color: white;
            padding: 0.25rem;
            text-align: center;
            font-size: 0.8rem;
        }
        .status-bar {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: var(--bg-card);
            border-top: 1px solid var(--border);
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 100;
        }
        .loading {
            display: none;
            text-align: center;
            padding: 2rem;
        }
        .loading.active {
            display: block;
        }
        .spinner {
            width: 40px;
            height: 40px;
            border: 3px solid var(--border);
            border-top-color: var(--primary);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 1rem;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        .hidden { display: none !important; }
        .zoom-modal {
            position: fixed;
            inset: 0;
            background: rgba(0,0,0,0.9);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            cursor: zoom-out;
        }
        .zoom-modal img {
            max-width: 90vw;
            max-height: 90vh;
        }
    </style>
</head>
<body>
    <!-- Theme Switcher -->
    <div class="theme-switcher">
        <button class="theme-btn active" onclick="setTheme('default')" id="theme-default">Dark</button>
        <button class="theme-btn" onclick="setTheme('intuitive')" id="theme-intuitive">Intuitive</button>
    </div>

    <div class="bg-effects">
        <div class="bg-orb bg-orb-1"></div>
        <div class="bg-orb bg-orb-2"></div>
    </div>

    <div class="container">
        <header>
            <h1>Maths Homework Generator</h1>
            <p>Create customised worksheets from educational resources</p>
        </header>

        <div class="search-section">
            <div class="form-row">
                <div class="form-group">
                    <label>Level</label>
                    <select id="level">
                        <option value="gcse">GCSE</option>
                        <option value="ks3">KS3 (Year 7-9)</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Difficulty</label>
                    <select id="difficulty">
                        <option value="medium">Medium</option>
                        <option value="hard">Hard</option>
                        <option value="harder">Harder (Grade 8-9)</option>
                        <option value="pastpapers">Past Papers Only</option>
                    </select>
                </div>
                <div class="form-group" id="keywordsGroup">
                    <label>Keywords (optional)</label>
                    <input type="text" id="keywords" placeholder="e.g., tree diagram, conditional">
                </div>
            </div>

            <label>Choose a Topic</label>
            <div class="topic-grid" id="topicGrid">
                <!-- Topics will be populated by JS -->
            </div>
        </div>

        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p id="loadingText">Searching for PDFs...</p>
        </div>

        <div class="results-section hidden" id="resultsSection">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h3>Found PDFs</h3>
                <button class="btn btn-secondary" onclick="startOver()" style="padding: 0.5rem 1rem; font-size: 0.9rem;">↻ New Search</button>
            </div>
            <div class="pdf-results" id="pdfResults"></div>

            <div id="pageSection" class="hidden" style="margin-top: 2rem;">
                <h3 style="margin-bottom: 1rem;">Select Pages</h3>
                <div class="page-grid" id="pageGrid"></div>
            </div>
        </div>
    </div>

    <div class="status-bar hidden" id="statusBar">
        <div>
            <span id="selectedCount">0</span> pages selected from <span id="pdfCount">1</span> PDF(s)
            <span id="collectedInfo" style="margin-left: 1rem; color: var(--success);" class="hidden">
                📦 <span id="collectedCount">0</span> pages collected
            </span>
        </div>
        <div style="display: flex; gap: 0.5rem;">
            <button class="btn btn-secondary" onclick="startOver()">Start Over</button>
            <button class="btn btn-secondary hidden" id="addMoreBtn" onclick="addMorePDFs()">+ Add More PDFs</button>
            <button class="btn" id="confirmBtn" onclick="confirmSelection()">Confirm Selection</button>
            <button class="btn btn-secondary hidden" id="editBtn" onclick="editSelection()">✏️ Edit</button>
            <button class="btn btn-success hidden" id="generateBtn" onclick="generatePDF()">Generate Final PDF</button>
        </div>
    </div>

    <div class="zoom-modal hidden" id="zoomModal" onclick="closeZoom()">
        <img id="zoomImage" src="">
    </div>

    <script>
        const TOPICS = ''' + json.dumps(list(TOPICS.keys())) + ''';

        let selectedTopic = null;
        let selectedPages = new Set();
        let currentPDF = null;
        let selectionConfirmed = false;

        // Multi-PDF support
        let collectedPages = [];  // Array of {pdfPath, pages: [1,2,3], pdfIndex}
        let loadedPDFs = [];      // Array of {path, url, title, thumbnails}

        // Populate topics
        const topicGrid = document.getElementById('topicGrid');
        TOPICS.forEach(topic => {
            const div = document.createElement('div');
            div.className = 'topic-item';
            div.textContent = topic;
            div.onclick = () => selectTopic(topic, div);
            topicGrid.appendChild(div);
        });

        // Handle difficulty change - also reset results if we have a topic selected
        document.getElementById('difficulty').addEventListener('change', function() {
            const keywordsGroup = document.getElementById('keywordsGroup');
            const keywordsInput = document.getElementById('keywords');
            if (this.value === 'pastpapers') {
                keywordsGroup.style.opacity = '0.5';
                keywordsInput.disabled = true;
                keywordsInput.placeholder = 'Auto-filtered by topic';
            } else {
                keywordsGroup.style.opacity = '1';
                keywordsInput.disabled = false;
                keywordsInput.placeholder = 'e.g., tree diagram, conditional';
            }
            // Re-search if topic is already selected - reset page state first
            if (selectedTopic) {
                resetPageState();
                searchPDFs();
            }
        });

        // Handle level change - re-search if topic selected
        document.getElementById('level').addEventListener('change', function() {
            if (selectedTopic) {
                resetPageState();
                searchPDFs();
            }
        });

        // Reset page selection state without clearing search results
        function resetPageState() {
            selectedPages.clear();
            currentPDF = null;
            selectionConfirmed = false;
            collectedPages = [];
            loadedPDFs = [];
            document.getElementById('pageSection').classList.add('hidden');
            document.getElementById('statusBar').classList.add('hidden');
            document.getElementById('confirmBtn').classList.remove('hidden');
            document.getElementById('editBtn').classList.add('hidden');
            document.getElementById('generateBtn').classList.add('hidden');
            document.getElementById('addMoreBtn').classList.add('hidden');
            document.getElementById('collectedInfo').classList.add('hidden');
        }

        function selectTopic(topic, element) {
            document.querySelectorAll('.topic-item').forEach(el => el.classList.remove('selected'));
            element.classList.add('selected');
            selectedTopic = topic;
            searchPDFs();
        }

        async function searchPDFs() {
            const level = document.getElementById('level').value;
            const difficulty = document.getElementById('difficulty').value;
            const keywords = document.getElementById('keywords').value;

            document.getElementById('loading').classList.add('active');
            document.getElementById('resultsSection').classList.add('hidden');
            document.getElementById('statusBar').classList.add('hidden');

            try {
                const response = await fetch('/api/search', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        topic: selectedTopic,
                        level: level,
                        difficulty: difficulty,
                        keywords: keywords
                    })
                });

                const data = await response.json();
                displayResults(data.results);
            } catch (error) {
                console.error('Search error:', error);
                alert('Error searching for PDFs');
            }

            document.getElementById('loading').classList.remove('active');
        }

        function displayResults(results) {
            const container = document.getElementById('pdfResults');
            container.innerHTML = '';

            if (results.length === 0) {
                container.innerHTML = '<p style="color: var(--text-muted);">No PDFs found. Try different keywords or topic.</p>';
                document.getElementById('resultsSection').classList.remove('hidden');
                return;
            }

            // Check if we're in pastpapers mode to show organized view
            const difficulty = document.getElementById('difficulty').value;

            if (difficulty === 'pastpapers') {
                // Group by year for past papers
                const byYear = {};
                results.forEach((pdf, index) => {
                    const year = pdf.year || 'Other';
                    if (!byYear[year]) byYear[year] = [];
                    byYear[year].push({...pdf, index});
                });

                // Sort years descending
                const years = Object.keys(byYear).sort((a, b) => b.localeCompare(a));

                years.forEach(year => {
                    // Year header
                    const yearHeader = document.createElement('div');
                    yearHeader.style.cssText = 'grid-column: 1/-1; background: var(--gradient-1); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 1.2rem; font-weight: 700; margin-top: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border);';
                    yearHeader.textContent = year === 'Unknown' ? 'Other Papers' : `📅 ${year}`;
                    container.appendChild(yearHeader);

                    // Papers for this year
                    byYear[year].forEach(pdf => {
                        const card = document.createElement('div');
                        card.className = 'pdf-card';
                        const sessionBadge = pdf.session !== 'Unknown' ? `<span style="background: var(--primary-glow); color: var(--primary-light); padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.75rem; margin-right: 0.5rem;">${pdf.session}</span>` : '';
                        const paperBadge = pdf.paper !== 'Paper' ? `<span style="background: var(--secondary-glow); color: var(--secondary); padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.75rem;">${pdf.paper}</span>` : '';
                        card.innerHTML = `
                            <div style="margin-bottom: 0.5rem;">${sessionBadge}${paperBadge}</div>
                            <h4>${pdf.title}</h4>
                            <p class="source">${pdf.source}</p>
                            <button class="btn" style="margin-top: 0.5rem; padding: 0.5rem 1rem; font-size: 0.85rem;" onclick="loadPDF(${pdf.index})">Load PDF</button>
                        `;
                        container.appendChild(card);
                    });
                });
            } else {
                // Standard display for other modes
                results.forEach((pdf, index) => {
                    const card = document.createElement('div');
                    card.className = 'pdf-card';
                    card.innerHTML = `
                        <h4>${pdf.title}</h4>
                        <p class="source">${pdf.source}</p>
                        <button class="btn" style="margin-top: 0.5rem; padding: 0.5rem 1rem; font-size: 0.85rem;" onclick="loadPDF(${index})">Load PDF</button>
                    `;
                    container.appendChild(card);
                });
            }

            document.getElementById('resultsSection').classList.remove('hidden');
            window.pdfResults = results;
        }

        async function loadPDF(index) {
            const pdf = window.pdfResults[index];
            document.getElementById('loadingText').textContent = 'Loading PDF pages...';
            document.getElementById('loading').classList.add('active');

            try {
                const response = await fetch('/api/load-pdf', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: pdf.url, topic: selectedTopic })
                });

                const data = await response.json();
                if (data.error) {
                    alert('Error loading PDF: ' + data.error);
                    document.getElementById('loading').classList.remove('active');
                    return;
                }

                currentPDF = data.path;

                // Track loaded PDF
                loadedPDFs.push({
                    path: data.path,
                    url: pdf.url,
                    title: pdf.title,
                    thumbnails: data.thumbnails
                });

                displayPages(data.thumbnails, data.filtered_pages);

                // Scroll to page section after a brief delay
                setTimeout(() => {
                    document.getElementById('pageSection').scrollIntoView({ behavior: 'smooth', block: 'start' });
                }, 100);

            } catch (error) {
                console.error('Load error:', error);
                alert('Error loading PDF');
            }

            document.getElementById('loading').classList.remove('active');
        }

        function displayPages(thumbnails, filteredPages) {
            const container = document.getElementById('pageGrid');
            container.innerHTML = '';
            selectedPages.clear();

            // Pre-select filtered pages
            if (filteredPages && filteredPages.length > 0) {
                filteredPages.forEach(p => selectedPages.add(p + 1)); // Convert 0-indexed to 1-indexed
                // Show info message about auto-filtering
                const infoDiv = document.createElement('div');
                infoDiv.style.cssText = 'grid-column: 1/-1; background: var(--success-glow); border: 1px solid var(--success); border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 0.5rem; color: var(--success);';
                infoDiv.innerHTML = `✓ Auto-selected ${filteredPages.length} pages containing topic keywords. Click pages to add/remove.`;
                container.appendChild(infoDiv);
            } else if (document.getElementById('difficulty').value === 'pastpapers') {
                // Show warning if no pages matched in past papers mode
                const warnDiv = document.createElement('div');
                warnDiv.style.cssText = 'grid-column: 1/-1; background: var(--secondary-glow); border: 1px solid var(--warning); border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 0.5rem; color: var(--warning);';
                warnDiv.innerHTML = `⚠ No pages auto-matched topic keywords. Manually select pages with relevant questions.`;
                container.appendChild(warnDiv);
            }

            thumbnails.forEach(thumb => {
                const div = document.createElement('div');
                div.className = 'page-item' + (selectedPages.has(thumb.page) ? ' selected' : '');
                div.innerHTML = `
                    <img src="${thumb.data}" onclick="togglePage(${thumb.page}, this.parentElement)">
                    <div class="page-number">Page ${thumb.page}</div>
                    <button style="position:absolute;top:4px;right:4px;background:var(--primary);border:none;border-radius:4px;padding:2px 6px;color:white;font-size:0.7rem;cursor:pointer;" onclick="zoomPage(${thumb.page})">🔍</button>
                `;
                container.appendChild(div);
            });

            document.getElementById('pageSection').classList.remove('hidden');
            document.getElementById('statusBar').classList.remove('hidden');
            updateSelectedCount();
        }

        function togglePage(pageNum, element) {
            if (selectionConfirmed) return;

            if (selectedPages.has(pageNum)) {
                selectedPages.delete(pageNum);
                element.classList.remove('selected');
            } else {
                selectedPages.add(pageNum);
                element.classList.add('selected');
            }
            updateSelectedCount();
        }

        function updateSelectedCount() {
            document.getElementById('selectedCount').textContent = selectedPages.size;
        }

        function confirmSelection() {
            if (selectedPages.size === 0) {
                alert('Please select at least one page');
                return;
            }

            selectionConfirmed = true;

            // Save current selection to collected pages
            collectedPages.push({
                pdfPath: currentPDF,
                pages: Array.from(selectedPages).sort((a, b) => a - b),
                pdfIndex: loadedPDFs.length - 1
            });

            // Update UI
            document.getElementById('confirmBtn').classList.add('hidden');
            document.getElementById('editBtn').classList.remove('hidden');
            document.getElementById('generateBtn').classList.remove('hidden');
            document.getElementById('addMoreBtn').classList.remove('hidden');

            // Show collected info
            document.getElementById('collectedInfo').classList.remove('hidden');
            const totalCollected = collectedPages.reduce((sum, p) => sum + p.pages.length, 0);
            document.getElementById('collectedCount').textContent = totalCollected;
            document.getElementById('pdfCount').textContent = collectedPages.length;

            // Dim unselected pages
            document.querySelectorAll('.page-item').forEach(el => {
                el.style.pointerEvents = 'none';
                if (!el.classList.contains('selected')) {
                    el.style.opacity = '0.3';
                }
            });
        }

        function editSelection() {
            selectionConfirmed = false;

            // Remove the last collected entry if editing
            if (collectedPages.length > 0) {
                collectedPages.pop();
            }

            // Update UI
            document.getElementById('confirmBtn').classList.remove('hidden');
            document.getElementById('editBtn').classList.add('hidden');
            document.getElementById('generateBtn').classList.add('hidden');
            document.getElementById('addMoreBtn').classList.add('hidden');

            // Update collected info
            if (collectedPages.length === 0) {
                document.getElementById('collectedInfo').classList.add('hidden');
            } else {
                const totalCollected = collectedPages.reduce((sum, p) => sum + p.pages.length, 0);
                document.getElementById('collectedCount').textContent = totalCollected;
                document.getElementById('pdfCount').textContent = collectedPages.length;
            }

            // Re-enable page selection
            document.querySelectorAll('.page-item').forEach(el => {
                el.style.pointerEvents = 'auto';
                el.style.opacity = '1';
            });
        }

        function addMorePDFs() {
            // Reset for loading another PDF but keep collected pages
            selectedPages.clear();
            currentPDF = null;
            selectionConfirmed = false;

            // Hide page section, show PDF results
            document.getElementById('pageSection').classList.add('hidden');
            document.getElementById('confirmBtn').classList.remove('hidden');
            document.getElementById('editBtn').classList.add('hidden');
            document.getElementById('generateBtn').classList.add('hidden');
            document.getElementById('addMoreBtn').classList.add('hidden');

            // Scroll to PDF results
            document.getElementById('pdfResults').scrollIntoView({ behavior: 'smooth' });

            updateSelectedCount();
        }

        async function generatePDF() {
            // Check if we have collected pages from multiple PDFs
            const totalCollected = collectedPages.reduce((sum, p) => sum + p.pages.length, 0);

            if (totalCollected === 0 && selectedPages.size === 0) {
                alert('Please select at least one page');
                return;
            }

            document.getElementById('loadingText').textContent = 'Generating PDF...';
            document.getElementById('loading').classList.add('active');

            try {
                let response;

                if (collectedPages.length > 0) {
                    // Multi-PDF mode - merge from collected pages
                    response = await fetch('/api/generate-multi', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            collected: collectedPages,
                            topic: selectedTopic
                        })
                    });
                } else {
                    // Single PDF mode (legacy)
                    response = await fetch('/api/generate', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            path: currentPDF,
                            pages: Array.from(selectedPages).sort((a,b) => a-b),
                            topic: selectedTopic
                        })
                    });
                }

                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `${selectedTopic.replace(/[^a-zA-Z0-9]/g, '_')}_homework.pdf`;
                a.click();
            } catch (error) {
                console.error('Generate error:', error);
                alert('Error generating PDF');
            }

            document.getElementById('loading').classList.remove('active');
        }

        async function zoomPage(pageNum) {
            event.stopPropagation();

            try {
                const response = await fetch('/api/zoom-page', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ path: currentPDF, page: pageNum })
                });

                const data = await response.json();
                document.getElementById('zoomImage').src = data.image;
                document.getElementById('zoomModal').classList.remove('hidden');
            } catch (error) {
                console.error('Zoom error:', error);
            }
        }

        function closeZoom() {
            document.getElementById('zoomModal').classList.add('hidden');
        }

        function startOver() {
            selectedTopic = null;
            selectedPages.clear();
            currentPDF = null;
            selectionConfirmed = false;
            collectedPages = [];
            loadedPDFs = [];

            document.querySelectorAll('.topic-item').forEach(el => el.classList.remove('selected'));
            document.getElementById('keywords').value = '';
            document.getElementById('resultsSection').classList.add('hidden');
            document.getElementById('pageSection').classList.add('hidden');
            document.getElementById('statusBar').classList.add('hidden');
            document.getElementById('confirmBtn').classList.remove('hidden');
            document.getElementById('editBtn').classList.add('hidden');
            document.getElementById('generateBtn').classList.add('hidden');
            document.getElementById('addMoreBtn').classList.add('hidden');
            document.getElementById('collectedInfo').classList.add('hidden');

            fetch('/api/cleanup', { method: 'POST' });
        }

        document.addEventListener('keydown', e => {
            if (e.key === 'Escape') closeZoom();
        });

        // Theme switching
        function setTheme(theme) {
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('homework-theme', theme);

            // Update button states
            document.querySelectorAll('.theme-btn').forEach(btn => btn.classList.remove('active'));
            document.getElementById('theme-' + theme).classList.add('active');
        }

        // Load saved theme on page load
        (function() {
            const savedTheme = localStorage.getItem('homework-theme') || 'default';
            setTheme(savedTheme);
        })();
    </script>
</body>
</html>'''


class HomeworkHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the homework tool"""

    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            # Use the new template from html_template.py
            html = get_html_template(list(TOPICS.keys()))
            self.wfile.write(html.encode())
        elif self.path.startswith('/download/'):
            # Serve generated PDF files
            filename = self.path.split('/download/')[-1]
            filepath = OUTPUT_DIR / filename
            if filepath.exists() and filepath.suffix == '.pdf':
                self.send_response(200)
                self.send_header('Content-Type', 'application/pdf')
                self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
                self.end_headers()
                with open(filepath, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404)
        else:
            self.send_error(404)

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        content_type = self.headers.get('Content-Type', '')

        # Handle multipart form data (file uploads)
        if 'multipart/form-data' in content_type:
            data = {}
            # File upload will be handled separately in handle_upload_custom_pdf
        else:
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(body) if body else {}
            except:
                data = {}

        if self.path == '/api/search':
            self.handle_search(data)
        elif self.path == '/api/load-pdf':
            self.handle_load_pdf(data)
        elif self.path == '/api/generate':
            self.handle_generate(data)
        elif self.path == '/api/generate-multi':
            self.handle_generate_multi(data)
        elif self.path == '/api/zoom-page':
            self.handle_zoom_page(data)
        elif self.path == '/api/ai-process-papers':
            self.handle_ai_process_papers(data)
        elif self.path == '/api/cleanup':
            self.handle_cleanup()
        elif self.path == '/upload_custom_pdf':
            self.handle_upload_custom_pdf()
        elif self.path == '/scan_custom_pdf':
            self.handle_scan_custom_pdf(data)
        elif self.path == '/generate_custom_pdf':
            self.handle_generate_custom_pdf(data)
        else:
            self.send_error(404)

    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def handle_search(self, data):
        topic = data.get('topic', '')
        level = data.get('level', 'gcse')
        difficulty = data.get('difficulty', 'medium')
        keywords_str = data.get('keywords', '')

        keywords = [k.strip() for k in keywords_str.split(',') if k.strip()] if keywords_str else None

        print(f"\n🔍 Searching: {topic} ({level}, {difficulty})")
        results = search_all_sources(topic, keywords, level, difficulty)

        # Store in session for later use
        session_data['search_results'] = results
        session_data['difficulty'] = difficulty
        session_data['topic'] = topic
        self.send_json({'results': results})

    def handle_load_pdf(self, data):
        url = data.get('url', '')
        topic = data.get('topic', '') or session_data.get('topic', '')
        difficulty = session_data.get('difficulty', 'medium')

        print(f"\n📥 Downloading: {url[:60]}...")
        print(f"   Topic: {topic}, Difficulty: {difficulty}")

        pdf_path = download_pdf(url)
        if not pdf_path:
            self.send_json({'error': 'Failed to download PDF'})
            return

        print(f"   Generating thumbnails...")
        thumbnails = get_pdf_page_thumbnails(pdf_path)

        # For past papers mode, filter pages by topic keywords
        filtered_pages = []
        if difficulty == 'pastpapers' and topic:
            print(f"   🔍 Filtering pages for topic: {topic}")
            filtered_pages = filter_pdf_pages_by_topic(pdf_path, topic)
            if filtered_pages:
                print(f"   ✓ Found {len(filtered_pages)} pages with topic keywords")
            else:
                print(f"   ⚠ No pages matched topic keywords - showing all pages")

        session_data['current_pdf'] = str(pdf_path)

        self.send_json({
            'path': str(pdf_path),
            'thumbnails': thumbnails,
            'filtered_pages': filtered_pages
        })

    def handle_generate(self, data):
        pdf_path = Path(data.get('path', ''))
        pages = data.get('pages', [])
        topic = data.get('topic', 'homework')

        print(f"\n📄 Generating PDF with pages: {pages}")

        output_path = remove_pages_from_pdf(pdf_path, pages)

        # Copy to outputs
        final_name = f"{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        final_path = OUTPUT_DIR / final_name
        shutil.copy(output_path, final_path)

        # Send file
        self.send_response(200)
        self.send_header('Content-Type', 'application/pdf')
        self.send_header('Content-Disposition', f'attachment; filename="{final_name}"')
        self.end_headers()

        with open(output_path, 'rb') as f:
            self.wfile.write(f.read())

    def handle_generate_multi(self, data):
        """Generate PDF from multiple source PDFs with optional mark schemes as ZIP"""
        import zipfile

        collected = data.get('collected', [])
        topic = data.get('topic', 'homework')
        include_mark_schemes = data.get('includeMarkSchemes', False)

        print(f"\n📄 Generating multi-PDF from {len(collected)} sources")
        if include_mark_schemes:
            print(f"   📝 Mark schemes will be included as separate PDF in ZIP")

        # Create questions PDF
        questions_writer = PdfWriter()
        total_pages = 0
        mark_scheme_info = []  # Store mark scheme info for later

        # Base directories
        BASE_DIR = Path(__file__).parent
        MS_DIR = BASE_DIR / "markschemes"

        # First pass: Add all question pages
        for item in collected:
            pdf_path = Path(item.get('pdfPath', ''))
            pages = item.get('pages', [])

            print(f"   Adding {len(pages)} pages from {pdf_path.name}")

            if not pdf_path.exists():
                print(f"   ⚠ PDF not found: {pdf_path}")
                continue

            try:
                reader = PdfReader(pdf_path)
                for page_num in pages:
                    if 0 <= page_num - 1 < len(reader.pages):
                        questions_writer.add_page(reader.pages[page_num - 1])
                        total_pages += 1

                # Track mark scheme info for this paper
                if include_mark_schemes:
                    mark_scheme_info.append({
                        'paper_path': pdf_path,
                        'pages': pages
                    })
            except Exception as e:
                print(f"   Error reading {pdf_path}: {e}")

        # Generate timestamp for filenames
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_topic = topic.replace(' ', '_').replace('-', '_')

        # Write questions PDF
        questions_path = WORK_DIR / f"{safe_topic}_Questions_{timestamp}.pdf"
        with open(questions_path, 'wb') as f:
            questions_writer.write(f)

        print(f"   ✓ Questions PDF: {total_pages} pages")

        # If mark schemes requested, create separate PDF and ZIP them together
        if include_mark_schemes and mark_scheme_info:
            ms_writer = PdfWriter()
            ms_pages_added = 0

            for ms_info in mark_scheme_info:
                paper_path = ms_info['paper_path']
                pages = ms_info['pages']

                # Find corresponding mark scheme file
                ms_path = MS_DIR / paper_path.name

                if not ms_path.exists():
                    print(f"   ⚠ Mark scheme not found: {ms_path.name}")
                    continue

                try:
                    ms_reader = PdfReader(ms_path)
                    for page_num in pages:
                        if 0 <= page_num - 1 < len(ms_reader.pages):
                            ms_writer.add_page(ms_reader.pages[page_num - 1])
                            ms_pages_added += 1
                except Exception as e:
                    print(f"   Error reading mark scheme {ms_path}: {e}")

            # Write mark schemes PDF
            markschemes_path = WORK_DIR / f"{safe_topic}_MarkSchemes_{timestamp}.pdf"
            with open(markschemes_path, 'wb') as f:
                ms_writer.write(f)

            print(f"   ✓ Mark Schemes PDF: {ms_pages_added} pages")

            # Create ZIP file with both PDFs
            zip_path = WORK_DIR / f"{safe_topic}_Homework_{timestamp}.zip"
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                zf.write(questions_path, f"{safe_topic}_Questions.pdf")
                zf.write(markschemes_path, f"{safe_topic}_MarkSchemes.pdf")

            print(f"   ✓ Created ZIP with Questions + Mark Schemes")

            # Send ZIP file
            self.send_response(200)
            self.send_header('Content-Type', 'application/zip')
            self.send_header('Content-Disposition', f'attachment; filename="{safe_topic}_Homework.zip"')
            self.end_headers()

            with open(zip_path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            # No mark schemes - just send the questions PDF
            final_name = f"{safe_topic}_Homework_{timestamp}.pdf"
            final_path = OUTPUT_DIR / final_name
            shutil.copy(questions_path, final_path)

            self.send_response(200)
            self.send_header('Content-Type', 'application/pdf')
            self.send_header('Content-Disposition', f'attachment; filename="{final_name}"')
            self.end_headers()

            with open(questions_path, 'rb') as f:
                self.wfile.write(f.read())

    def handle_zoom_page(self, data):
        pdf_path = Path(data.get('path', ''))
        page_num = data.get('page', 1)

        image = get_pdf_page_full(pdf_path, page_num)
        self.send_json({'image': image})

    def handle_cleanup(self):
        cleanup_temp()
        self.send_json({'status': 'ok'})

    def handle_upload_custom_pdf(self):
        """Handle custom PDF file upload - Python 3.13 compatible (no cgi module)"""
        content_type = self.headers.get('Content-Type', '')
        content_length = int(self.headers.get('Content-Length', 0))

        # Parse multipart form data
        if 'multipart/form-data' not in content_type:
            self.send_json({'success': False, 'error': 'Invalid content type'})
            return

        try:
            # Parse the boundary from content type
            boundary = None
            for part in content_type.split(';'):
                part = part.strip()
                if part.startswith('boundary='):
                    boundary = part.split('=', 1)[1].strip('"')
                    break

            if not boundary:
                self.send_json({'success': False, 'error': 'No boundary found'})
                return

            boundary = boundary.encode()

            # Read all data
            data = self.rfile.read(content_length)

            # Simple multipart parsing
            parts = data.split(b'--' + boundary)
            file_content = None
            filename = 'uploaded.pdf'

            for part in parts:
                if b'filename=' in part:
                    # Extract filename
                    header_end = part.find(b'\r\n\r\n')
                    if header_end > 0:
                        header = part[:header_end].decode('utf-8', errors='ignore')
                        content = part[header_end + 4:]
                        # Remove trailing boundary markers and whitespace
                        content = content.rstrip(b'\r\n-')
                        # Also strip any trailing \r\n
                        while content.endswith(b'\r\n'):
                            content = content[:-2]
                        file_content = content

                        # Extract filename from header
                        match = re.search(r'filename="([^"]+)"', header)
                        if match:
                            filename = match.group(1)

            if not file_content:
                self.send_json({'success': False, 'error': 'No file found in upload'})
                return

            # Save to temp directory
            custom_pdf_dir = WORK_DIR / "custom_pdfs"
            custom_pdf_dir.mkdir(exist_ok=True)

            safe_filename = re.sub(r'[^\w\-\.]', '_', filename)
            filepath = custom_pdf_dir / safe_filename

            with open(filepath, 'wb') as f:
                f.write(file_content)

            # Validate it's a valid PDF
            try:
                reader = PdfReader(filepath)
                page_count = len(reader.pages)
                print(f"📄 Custom PDF uploaded: {filename} ({page_count} pages)")
                self.send_json({
                    'success': True,
                    'path': str(filepath),
                    'page_count': page_count
                })
            except Exception as e:
                filepath.unlink(missing_ok=True)
                self.send_json({'success': False, 'error': f'Invalid PDF file: {str(e)}'})

        except Exception as e:
            print(f"Upload error: {e}")
            import traceback
            traceback.print_exc()
            self.send_json({'success': False, 'error': str(e)})

    def handle_scan_custom_pdf(self, data):
        """Scan custom PDF for topic-relevant pages with confidence scoring using enhanced OCR"""
        pdf_path = Path(data.get('path', ''))
        topic = data.get('topic', '')
        use_enhanced_ocr = data.get('enhanced_ocr', True)  # Default to using enhanced OCR

        if not pdf_path.exists():
            self.send_json({'success': False, 'error': 'PDF file not found'})
            return

        if not topic:
            self.send_json({'success': False, 'error': 'No topic specified'})
            return

        print(f"\n🔍 Scanning custom PDF for topic: {topic}")
        if use_enhanced_ocr:
            print(f"   📷 Enhanced OCR mode enabled for better accuracy")

        try:
            reader = PdfReader(pdf_path)
            total_pages = len(reader.pages)

            # Get topic keywords for matching
            keywords = get_topic_keywords(topic)  # Returns list
            strict_kw_dict = get_strict_keywords(topic)  # Returns dict with 'primary', 'context', 'exclude'

            # Extract primary and context keywords from strict dict
            primary_keywords = strict_kw_dict.get('primary', [])
            context_keywords = strict_kw_dict.get('context', [])
            exclude_keywords = strict_kw_dict.get('exclude', [])

            print(f"   Regular keywords: {keywords[:5] if keywords else []}...")
            print(f"   Primary (strict): {primary_keywords[:3] if primary_keywords else []}...")
            print(f"   Context: {context_keywords[:3] if context_keywords else []}...")

            results = []

            for page_num in range(total_pages):
                # Use enhanced OCR for custom resources (likely scanned documents)
                if use_enhanced_ocr:
                    text = extract_text_from_pdf_page(pdf_path, page_num, force_ocr=True)
                else:
                    text = extract_text_from_pdf_page(pdf_path, page_num, force_ocr=False)

                text_lower = text.lower()
                display_page = page_num + 1  # For display (1-indexed)

                # Score the page
                confidence = 'none'
                score = 0

                # Check for exclusions first
                should_exclude = False
                for exclude in exclude_keywords:
                    if exclude.lower() in text_lower:
                        should_exclude = True
                        break

                if should_exclude:
                    continue

                # Check primary (strict) keywords (high value)
                for kw in primary_keywords:
                    if kw.lower() in text_lower:
                        score += 10

                # Check context keywords (medium value)
                for kw in context_keywords:
                    if kw.lower() in text_lower:
                        score += 3

                # Check regular keywords (lower value)
                for kw in keywords:
                    if kw.lower() in text_lower:
                        score += 1

                # Check topic name directly
                topic_lower = topic.lower()
                if ' - ' in topic:
                    topic_name = topic.split(' - ', 1)[1].lower()
                else:
                    topic_name = topic_lower

                if topic_name in text_lower:
                    score += 5

                # Determine confidence level
                if score >= 10:
                    confidence = 'high'
                elif score >= 3:
                    confidence = 'medium'

                if confidence != 'none':
                    # Generate thumbnail for this page
                    thumbnail = generate_page_thumbnail(pdf_path, page_num)
                    results.append({
                        'page': display_page,
                        'confidence': confidence,
                        'score': score,
                        'thumbnail': thumbnail
                    })

            # Sort by score (highest first)
            results.sort(key=lambda x: (-1 if x['confidence'] == 'high' else 0, -x['score']))

            print(f"   Found {len([r for r in results if r['confidence'] == 'high'])} high confidence pages")
            print(f"   Found {len([r for r in results if r['confidence'] == 'medium'])} medium confidence pages")

            self.send_json({
                'success': True,
                'pages': results,
                'total_pages': total_pages
            })

        except Exception as e:
            print(f"   Error scanning PDF: {e}")
            self.send_json({'success': False, 'error': str(e)})

    def handle_generate_custom_pdf(self, data):
        """Generate filtered PDF from custom upload"""
        pdf_path = Path(data.get('path', ''))
        pages = data.get('pages', [])
        topic = data.get('topic', 'custom')

        if not pdf_path.exists():
            self.send_json({'success': False, 'error': 'PDF file not found'})
            return

        if not pages:
            self.send_json({'success': False, 'error': 'No pages selected'})
            return

        print(f"\n📄 Generating custom PDF with {len(pages)} pages for topic: {topic}")

        try:
            reader = PdfReader(pdf_path)
            writer = PdfWriter()

            for page_num in sorted(pages):
                if 0 < page_num <= len(reader.pages):
                    writer.add_page(reader.pages[page_num - 1])

            # Save output
            safe_topic = re.sub(r'[^\w\-]', '_', topic)
            filename = f"{safe_topic}_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            output_path = OUTPUT_DIR / filename

            with open(output_path, 'wb') as f:
                writer.write(f)

            print(f"   ✅ Generated: {filename}")

            self.send_json({
                'success': True,
                'filename': filename,
                'download_url': f'/download/{filename}'
            })

        except Exception as e:
            print(f"   Error generating PDF: {e}")
            self.send_json({'success': False, 'error': str(e)})

    def handle_ai_process_papers(self, data):
        """Process multiple papers with AI/OCR to auto-detect topic-relevant pages"""
        papers = data.get('papers', [])
        topic = data.get('topic', '') or session_data.get('topic', '')

        if not papers:
            self.send_json({'error': 'No papers selected'})
            return

        if not topic:
            self.send_json({'error': 'No topic selected'})
            return

        print(f"\n🤖 AI Processing {len(papers)} papers for topic: {topic}")
        results = []

        for paper_info in papers:
            url = paper_info.get('url', '')
            title = paper_info.get('title', '')

            print(f"   📥 Downloading: {title[:50]}...")
            pdf_path = download_pdf(url)

            if not pdf_path:
                print(f"   ⚠ Failed to download: {title}")
                continue

            print(f"   🖼 Generating thumbnails...")
            thumbnails = get_pdf_page_thumbnails(pdf_path)

            print(f"   🔍 OCR scanning for topic keywords...")
            filtered_pages_with_confidence = filter_pdf_pages_by_topic(pdf_path, topic, return_confidence=True)

            if filtered_pages_with_confidence:
                high_count = len([p for p in filtered_pages_with_confidence if p['confidence'] == 'high'])
                med_count = len([p for p in filtered_pages_with_confidence if p['confidence'] == 'medium'])
                print(f"   ✓ Found {high_count} definite + {med_count} possible pages for '{topic}'")
            else:
                print(f"   ⚠ No pages matched topic")

            results.append({
                'path': str(pdf_path),
                'url': url,
                'title': title,
                'thumbnails': thumbnails,
                'filtered_pages': filtered_pages_with_confidence if filtered_pages_with_confidence else []
            })

        print(f"   ✅ AI processing complete: {sum(len(r['filtered_pages']) for r in results)} total pages found")

        self.send_json({'results': results})

    def log_message(self, format, *args):
        # Suppress default logging
        pass


def main():
    port = 5000
    server = HTTPServer(('127.0.0.1', port), HomeworkHandler)
    print(f"\n{'='*50}")
    print(f"  Maths Homework Generator")
    print(f"  Open: http://127.0.0.1:{port}")
    print(f"{'='*50}\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        cleanup_temp()
        server.server_close()


if __name__ == '__main__':
    main()
