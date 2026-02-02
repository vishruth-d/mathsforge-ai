# MathsForge AI

**AI-powered GCSE Maths worksheet generator** - Create customised homework worksheets from Edexcel past papers and custom resources with intelligent topic detection.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)

## Features

- 📚 **Smart Topic Detection** - AI-powered OCR scans PDFs to find relevant questions by topic
- 🎯 **38 GCSE Topics** - Comprehensive coverage of Edexcel GCSE Maths syllabus
- 📄 **Custom Resources** - Upload your own textbooks/worksheets for scanning
- ✅ **Mark Scheme Support** - Automatically pairs questions with mark schemes
- 🎨 **Modern UI** - Sleek, dark-themed interface with custom cursor
- 📦 **ZIP Downloads** - Download questions and mark schemes as separate PDFs

## Installation

### Prerequisites

- Python 3.10+
- Tesseract OCR (for enhanced text detection)

### macOS

```bash
# Install Tesseract
brew install tesseract

# Clone the repo
git clone https://github.com/vishruth-d/mathsforge-ai.git
cd mathsforge-ai

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Windows

```batch
# Install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
# Add to PATH

# Clone and setup
git clone https://github.com/vishruth-d/mathsforge-ai.git
cd mathsforge-ai

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

## Usage

1. **Start the server:**
   ```bash
   cd src
   python web_app_v2.py
   ```

2. **Open in browser:**
   ```
   http://127.0.0.1:5000
   ```

3. **Add past papers:**
   - Place Edexcel past paper PDFs in `papers/` folder
   - Place corresponding mark schemes in `markschemes/` folder
   - Name format: `YYYY_Month_Paper_N.pdf` (e.g., `2023_Jun_Paper_1.pdf`)

4. **Generate worksheets:**
   - Select a topic from the dropdown
   - Choose difficulty level
   - Enable AI-Enhanced mode for automatic page detection
   - Click "Generate Worksheet"

## Project Structure

```
mathsforge-ai/
├── src/
│   ├── web_app_v2.py          # Main web server
│   ├── html_template.py        # Frontend HTML/CSS/JS
│   ├── strict_keywords.py      # Topic keyword definitions
│   ├── topic_keywords.py       # Extended keyword mappings
│   ├── train_keywords.py       # ML keyword training script
│   └── apply_learned_keywords.py
├── papers/                     # Past paper PDFs (not tracked)
├── markschemes/               # Mark scheme PDFs (not tracked)
├── training/                  # Topic-specific training data
│   ├── 01_number/
│   ├── 02_angles/
│   ├── ...
│   └── 38_trigonometric_graphs/
├── docs/                      # Documentation
├── requirements.txt
├── setup.sh                   # macOS/Linux setup
├── setup.bat                  # Windows setup
└── README.md
```

## Topics Covered (38 Total)

| # | Topic | # | Topic |
|---|-------|---|-------|
| 1 | Number (HCF, LCM, Primes) | 20 | Trigonometry |
| 2 | Angles | 21 | Bounds |
| 3 | Scatter Graphs | 22 | Vectors |
| 4 | Fractions | 23 | Reciprocal & Exponential Graphs |
| 5 | Expressions & Sequences | 24 | 3D Shapes & Volume |
| 6 | Coordinates | 25 | Probability |
| 7 | Percentages | 26 | Proportion |
| 8 | Linear Graphs | 27 | Loci & Constructions |
| 9 | Perimeter & Area | 28 | Algebraic Fractions |
| 10 | Transformations | 29 | Quadratic Graphs |
| 11 | Ratio | 30 | Circle Theorems |
| 12 | Right-angled Triangles | 31 | Quadratic Equations |
| 13 | Statistics | 32 | Simultaneous Equations |
| 14 | Congruence & Similarity | 33 | Functions |
| 15 | Linear Equations | 34 | Iteration |
| 16 | Inequalities | 35 | Proof |
| 17 | Circles | 36 | Gradients & Rate of Change |
| 18 | Indices & Surds | 37 | Pre-calculus |
| 19 | Pythagoras Theorem | 38 | Trigonometric Graphs |

## Training the Keyword System

MathsForge AI can learn better keywords from topic-specific papers:

1. **Add training data:**
   - Download topic-specific worksheets from Maths Genie, Corbett Maths, etc.
   - Place PDFs in the corresponding `training/XX_topic_name/` folder

2. **Run training:**
   ```bash
   python src/train_keywords.py
   ```

3. **Apply learned keywords:**
   ```bash
   python src/apply_learned_keywords.py
   ```

## Tech Stack

- **Backend:** Python `http.server` (no Flask dependency)
- **PDF Processing:** `pypdf`, `pypdfium2`, `pdfplumber`
- **OCR:** Tesseract via `pytesseract` with OpenCV preprocessing
- **Frontend:** Vanilla HTML/CSS/JS with modern dark theme

## License

All rights reserved. No license granted for use, modification, or distribution.

---

Built with ❤️ for GCSE Maths students
