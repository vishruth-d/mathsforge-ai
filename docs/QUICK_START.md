# Quick Start Guide

## 1. First Time Setup

### macOS
```bash
# Install Tesseract OCR
brew install tesseract

# Setup project
cd mathsforge-ai
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Windows
1. Download Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
2. Install and add to PATH
3. Run:
```batch
cd mathsforge-ai
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Add Past Papers

Place your Edexcel GCSE Maths past papers in the `papers/` folder.

**Naming convention:**
```
YYYY_Month_Paper_N.pdf
```

Examples:
- `2023_Jun_Paper_1.pdf`
- `2023_Jun_Paper_2.pdf`
- `2023_Nov_Paper_3.pdf`
- `2022_Jun_Paper_1.pdf`

## 3. Add Mark Schemes

Place mark schemes in the `markschemes/` folder with matching names:
- `2023_Jun_Paper_1_MS.pdf`
- `2023_Jun_Paper_2_MS.pdf`

## 4. Run the App

```bash
cd src
python web_app_v2.py
```

Open: http://127.0.0.1:5000

## 5. Generate Your First Worksheet

1. Select a **Topic** (e.g., "25 - Probability")
2. Choose **Difficulty** (Foundation/Higher/Mixed)
3. Toggle **AI-Enhanced Mode** ON
4. Select which **Past Papers** to scan
5. Click **"🔍 Scan with AI"**
6. Review detected pages, remove any false positives
7. Toggle **Include Mark Schemes** if wanted
8. Click **"Generate Worksheet"**
9. Download your PDF (or ZIP with mark schemes)

## Troubleshooting

### "tesseract is not installed"
- macOS: `brew install tesseract`
- Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki

### No pages detected
- Check your past papers are valid Edexcel PDFs
- Try a different topic
- Add more topic-specific keywords to `strict_keywords.py`

### Slow scanning
- Enhanced OCR is thorough but slower
- For quick results, use text-based PDFs (not scanned)
