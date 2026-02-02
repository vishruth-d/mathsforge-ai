#!/usr/bin/env python3
"""
MathsForge AI - Keyword Training System
Analyzes topic-specific papers to extract unique keywords and patterns.
"""

import os
import sys
import re
import json
from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, List, Set, Tuple

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    import pypdfium2 as pdfium
    from pypdf import PdfReader
    import pdfplumber
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Run: pip install pypdfium2 pypdf pdfplumber")
    sys.exit(1)

# Import enhanced OCR if available
try:
    from web_app_v2 import extract_text_from_pdf_page, extract_text_with_enhanced_ocr
    ENHANCED_OCR_AVAILABLE = True
except ImportError:
    ENHANCED_OCR_AVAILABLE = False
    print("Warning: Enhanced OCR not available, using basic extraction")

TRAINING_DIR = Path(__file__).parent / "training"
OUTPUT_FILE = Path(__file__).parent / "learned_keywords.json"

# Common words to ignore (stop words)
STOP_WORDS = {
    'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare',
    'ought', 'used', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by',
    'from', 'as', 'into', 'through', 'during', 'before', 'after', 'above',
    'below', 'between', 'under', 'again', 'further', 'then', 'once',
    'here', 'there', 'when', 'where', 'why', 'how', 'all', 'each', 'few',
    'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only',
    'own', 'same', 'so', 'than', 'too', 'very', 'just', 'and', 'but',
    'if', 'or', 'because', 'until', 'while', 'although', 'though',
    'this', 'that', 'these', 'those', 'what', 'which', 'who', 'whom',
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',
    'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his',
    'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
    'they', 'them', 'their', 'theirs', 'themselves', 'am', 'about',
    # Common exam words to ignore
    'marks', 'mark', 'total', 'answer', 'question', 'show', 'work',
    'working', 'diagram', 'figure', 'page', 'turn', 'over', 'write',
    'space', 'box', 'given', 'give', 'find', 'calculate', 'work out',
    'shown', 'shown below', 'complete', 'state', 'explain', 'describe',
    'hence', 'therefore', 'using', 'use', 'correct', 'decimal', 'places',
    'significant', 'figures', 'accurately', 'clearly', 'must', 'full',
}

# Mathematical symbols and patterns to look for
MATH_PATTERNS = {
    'equals': r'=',
    'not_equals': r'≠|!=',
    'less_than': r'<|&lt;',
    'greater_than': r'>|&gt;',
    'less_equal': r'≤|<=',
    'greater_equal': r'≥|>=',
    'plus_minus': r'±',
    'multiply': r'×|\\*',
    'divide': r'÷|/',
    'squared': r'²|\^2',
    'cubed': r'³|\^3',
    'square_root': r'√|sqrt',
    'pi': r'π|pi',
    'theta': r'θ|theta',
    'alpha': r'α|alpha',
    'beta': r'β|beta',
    'delta': r'Δ|δ|delta',
    'sigma': r'Σ|σ|sigma',
    'infinity': r'∞|infinity',
    'proportional': r'∝',
    'angle': r'∠|angle',
    'degree': r'°|degrees?',
    'arrow': r'→|->',
    'fraction_bar': r'/',
    'vector_notation': r'\\vec|→',
    'subscript': r'_\{?[a-z0-9]+\}?',
    'superscript': r'\^[\{\[]?[-]?[a-z0-9/]+[\}\]]?',
}


def extract_text_from_pdf(pdf_path: Path, use_ocr: bool = True) -> str:
    """Extract all text from a PDF using best available method"""
    all_text = []

    try:
        reader = PdfReader(pdf_path)
        num_pages = len(reader.pages)

        for page_num in range(num_pages):
            if ENHANCED_OCR_AVAILABLE and use_ocr:
                # Use enhanced OCR for better accuracy
                text = extract_text_from_pdf_page(pdf_path, page_num, force_ocr=True)
            else:
                # Fallback to pdfplumber
                try:
                    with pdfplumber.open(pdf_path) as pdf:
                        if page_num < len(pdf.pages):
                            text = pdf.pages[page_num].extract_text() or ""
                except:
                    text = reader.pages[page_num].extract_text() or ""

            all_text.append(text)

    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""

    return "\n".join(all_text)


def extract_ngrams(text: str, n: int = 2) -> List[str]:
    """Extract n-grams (word sequences) from text"""
    words = re.findall(r'\b[a-zA-Z]{2,}\b', text.lower())
    words = [w for w in words if w not in STOP_WORDS and len(w) > 2]

    ngrams = []
    for i in range(len(words) - n + 1):
        ngram = ' '.join(words[i:i+n])
        ngrams.append(ngram)

    return ngrams


def extract_math_patterns(text: str) -> Dict[str, int]:
    """Find mathematical symbols and patterns in text"""
    patterns_found = {}

    for name, pattern in MATH_PATTERNS.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            patterns_found[name] = len(matches)

    return patterns_found


def extract_unique_phrases(text: str) -> List[str]:
    """Extract potentially unique mathematical phrases"""
    phrases = []

    # Common maths phrase patterns
    phrase_patterns = [
        r'find the (\w+ ?){1,3}',
        r'calculate the (\w+ ?){1,3}',
        r'work out the (\w+ ?){1,3}',
        r'(\w+ ?){1,2} of the (\w+ ?){1,2}',
        r'in terms of (\w+)',
        r'express (\w+ ?){1,3} as',
        r'simplify (\w+ ?){1,3}',
        r'solve the (\w+ ?){1,2}',
        r'(\w+) = (\w+)',
        r'the (\w+) of (\w+)',
        r'is (\w+) to',
        r'(\w+) and (\w+)',
    ]

    for pattern in phrase_patterns:
        matches = re.findall(pattern, text.lower())
        for match in matches:
            if isinstance(match, tuple):
                phrase = ' '.join(m.strip() for m in match if m.strip())
            else:
                phrase = match.strip()
            if phrase and len(phrase) > 3:
                phrases.append(phrase)

    return phrases


def analyze_topic_folder(folder_path: Path) -> Dict:
    """Analyze all PDFs in a topic folder"""
    results = {
        'word_freq': Counter(),
        'bigrams': Counter(),
        'trigrams': Counter(),
        'math_patterns': Counter(),
        'phrases': Counter(),
        'total_docs': 0,
        'total_pages': 0,
    }

    pdf_files = list(folder_path.glob('*.pdf'))
    if not pdf_files:
        return results

    print(f"   Found {len(pdf_files)} PDFs")

    for pdf_path in pdf_files:
        print(f"      Processing: {pdf_path.name}")
        text = extract_text_from_pdf(pdf_path, use_ocr=True)

        if not text:
            continue

        results['total_docs'] += 1

        # Count pages (approximate by line breaks)
        results['total_pages'] += text.count('\n') // 50 + 1

        # Extract words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        words = [w for w in words if w not in STOP_WORDS]
        results['word_freq'].update(words)

        # Extract bigrams and trigrams
        results['bigrams'].update(extract_ngrams(text, 2))
        results['trigrams'].update(extract_ngrams(text, 3))

        # Extract math patterns
        patterns = extract_math_patterns(text)
        results['math_patterns'].update(patterns)

        # Extract phrases
        phrases = extract_unique_phrases(text)
        results['phrases'].update(phrases)

    return results


def find_unique_keywords(topic_data: Dict[str, Dict]) -> Dict[str, Dict]:
    """Find keywords that are unique to each topic (not common across all)"""

    # Get all words across all topics
    all_words = Counter()
    all_bigrams = Counter()
    all_trigrams = Counter()

    for topic, data in topic_data.items():
        all_words.update(data['word_freq'])
        all_bigrams.update(data['bigrams'])
        all_trigrams.update(data['trigrams'])

    unique_keywords = {}

    for topic, data in topic_data.items():
        if data['total_docs'] == 0:
            continue

        # Find words that appear more in this topic than others
        topic_unique_words = []
        for word, count in data['word_freq'].most_common(100):
            # Calculate uniqueness score
            total_count = all_words[word]
            topic_ratio = count / total_count if total_count > 0 else 0

            # If this topic has >50% of all occurrences, it's unique
            if topic_ratio > 0.5 and count >= 3:
                topic_unique_words.append({
                    'word': word,
                    'count': count,
                    'uniqueness': round(topic_ratio, 2)
                })

        # Same for bigrams
        topic_unique_bigrams = []
        for bigram, count in data['bigrams'].most_common(50):
            total_count = all_bigrams[bigram]
            topic_ratio = count / total_count if total_count > 0 else 0
            if topic_ratio > 0.4 and count >= 2:
                topic_unique_bigrams.append({
                    'phrase': bigram,
                    'count': count,
                    'uniqueness': round(topic_ratio, 2)
                })

        # Same for trigrams
        topic_unique_trigrams = []
        for trigram, count in data['trigrams'].most_common(30):
            total_count = all_trigrams[trigram]
            topic_ratio = count / total_count if total_count > 0 else 0
            if topic_ratio > 0.4 and count >= 2:
                topic_unique_trigrams.append({
                    'phrase': trigram,
                    'count': count,
                    'uniqueness': round(topic_ratio, 2)
                })

        unique_keywords[topic] = {
            'unique_words': topic_unique_words[:20],
            'unique_bigrams': topic_unique_bigrams[:15],
            'unique_trigrams': topic_unique_trigrams[:10],
            'math_patterns': dict(data['math_patterns'].most_common(10)),
            'common_phrases': [p for p, c in data['phrases'].most_common(15)],
            'stats': {
                'documents_analyzed': data['total_docs'],
                'pages_analyzed': data['total_pages'],
            }
        }

    return unique_keywords


def generate_keyword_suggestions(unique_keywords: Dict) -> Dict[str, Dict]:
    """Generate suggested keyword updates for strict_keywords.py"""

    suggestions = {}

    for topic, data in unique_keywords.items():
        if data['stats']['documents_analyzed'] == 0:
            continue

        # Extract high-confidence primary keywords
        primary_suggestions = []
        for item in data['unique_words']:
            if item['uniqueness'] >= 0.6:
                primary_suggestions.append(item['word'])

        for item in data['unique_bigrams']:
            if item['uniqueness'] >= 0.5:
                primary_suggestions.append(item['phrase'])

        for item in data['unique_trigrams']:
            if item['uniqueness'] >= 0.5:
                primary_suggestions.append(item['phrase'])

        # Context keywords (lower uniqueness threshold)
        context_suggestions = []
        for item in data['unique_words']:
            if 0.3 <= item['uniqueness'] < 0.6:
                context_suggestions.append(item['word'])

        suggestions[topic] = {
            'primary_suggestions': primary_suggestions[:15],
            'context_suggestions': context_suggestions[:10],
            'math_patterns': data['math_patterns'],
            'common_phrases': data['common_phrases'][:10],
        }

    return suggestions


def main():
    print("=" * 60)
    print("MathsForge AI - Keyword Training System")
    print("=" * 60)

    if not TRAINING_DIR.exists():
        print(f"Error: Training directory not found at {TRAINING_DIR}")
        print("Please create topic folders and add PDF files.")
        return

    # Find all topic folders
    topic_folders = sorted([
        f for f in TRAINING_DIR.iterdir()
        if f.is_dir() and not f.name.startswith('.')
    ])

    if not topic_folders:
        print("No topic folders found in training directory.")
        return

    print(f"\nFound {len(topic_folders)} topic folders")

    # Analyze each topic
    topic_data = {}
    for folder in topic_folders:
        topic_name = folder.name
        print(f"\n📚 Analyzing: {topic_name}")

        data = analyze_topic_folder(folder)
        topic_data[topic_name] = data

        if data['total_docs'] > 0:
            print(f"   ✅ {data['total_docs']} docs, ~{data['total_pages']} pages")
            print(f"   Top words: {[w for w, c in data['word_freq'].most_common(5)]}")

    # Find unique keywords per topic
    print("\n" + "=" * 60)
    print("Finding unique keywords per topic...")
    print("=" * 60)

    unique_keywords = find_unique_keywords(topic_data)

    # Generate suggestions
    suggestions = generate_keyword_suggestions(unique_keywords)

    # Save results
    output = {
        'unique_keywords': unique_keywords,
        'suggestions': suggestions,
        'metadata': {
            'total_topics': len(topic_folders),
            'topics_with_data': len([t for t in unique_keywords if unique_keywords[t]['stats']['documents_analyzed'] > 0])
        }
    }

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n✅ Results saved to: {OUTPUT_FILE}")

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY - Suggested Keywords by Topic")
    print("=" * 60)

    for topic, data in suggestions.items():
        print(f"\n📌 {topic}:")
        if data['primary_suggestions']:
            print(f"   PRIMARY: {data['primary_suggestions'][:5]}")
        if data['context_suggestions']:
            print(f"   CONTEXT: {data['context_suggestions'][:5]}")

    print("\n" + "=" * 60)
    print("Next steps:")
    print("1. Review learned_keywords.json")
    print("2. Add approved keywords to strict_keywords.py")
    print("3. Re-run to verify improvements")
    print("=" * 60)


if __name__ == "__main__":
    main()
