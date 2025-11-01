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

## =� Project Structure

```
roshn_module3/

