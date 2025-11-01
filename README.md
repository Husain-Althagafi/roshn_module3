# ROSHN PULSE - Module 3: Auto-Report Scribe

**AI-Powered NLP Service for Construction Daily Log Extraction**

---

##  Overview

Module 3 of the ROSHN PULSE MVP is an automated reporting engine that uses Natural Language Processing (NLP) to extract structured data from unstructured construction daily logs.

### Core Functionality

Extracts **3 key fields** from daily logs:
1. **Completed Tasks** - Work that was finished
2. **Blockers** - Issues preventing progress
3. **Incidents** - Safety incidents, quality issues, or notable events

### Technology Stack

- **NLP**: spaCy with en_core_web_sm model
- **API**: FastAPI with async support
- **PDF Generation**: ReportLab
- **Document Processing**: PyPDF2, python-docx
- **Data Validation**: Pydantic

---

##  Project Structure

```
roshn_module3/
      data/    
           sample_logs/       # 27 training samples (7 manual + 20 generated)
           reports/           # Generated PDF reports
           training/          # Training data
      schema.py              # Data schema definitions (LOCKED)
      extractor.py           # Core NLP extraction engine
      report_generator.py    # PDF report generator
      api.py                 # FastAPI service
      generate_logs.py       # Sample log generator
      requirements.txt       # Python dependencies
      README.md             # This file
```

---

##  Quick Start

### 1. Installation

```bash
# Install dependencies
uv pip install -r requirements.txt

# Download spaCy model
uv pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl
```

### 2. Test the Extractor

```bash
# Run extraction test
.venv/Scripts/python extractor.py
```

### 3. Test PDF Generation

```bash
# Generate sample report
.venv/Scripts/python report_generator.py
```

### 4. Start the API Server

```bash
# Start FastAPI server
.venv/Scripts/python api.py
```

Visit http://localhost:8000/docs for interactive API documentation.

---

##  API Endpoints

### Health Check
```
GET /health
```

### Extract from Text
```
POST /extract
Content-Type: application/json

{
  "text": "Daily log text here...",
  "generate_pdf": true
}
```

### Upload File
```
POST /upload
Content-Type: multipart/form-data

file: <file.txt|file.pdf|file.docx>
generate_pdf: true|false
```

### Download Report
```
GET /reports/{filename}
```

---

##  Testing

### Run All Tests

```bash
# Test extractor
.venv/Scripts/python extractor.py

# Test PDF generation
.venv/Scripts/python report_generator.py

# Test API (in another terminal)
.venv/Scripts/python api.py
```

---

##  Performance Targets

**MVP Success Criteria:**
-   Extract 3 key fields (tasks, blockers, incidents)
-   Process text/PDF/Word documents
-   Generate PDF reports
-   FastAPI endpoint operational
-    **Target: e85% F1 score** on field extraction

---

##  Author

**Husain** - Module 3 Developer
ROSHN Hackathon 2025 - Team PULSE
