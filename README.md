# CareerLens AI

CareerLens AI is an AI-assisted resume and job-description matching platform.

## Features
- Upload PDF/DOCX resumes
- Extract resume text
- Analyze job descriptions
- Detect technical skills
- Semantic resume-to-job similarity using Sentence Transformers
- Weighted job-match score
- Matched and missing skills
- Actionable improvement suggestions
- Clean browser dashboard

## Stack
Python, FastAPI, HTML, CSS, JavaScript, Sentence Transformers, scikit-learn, PyPDF, python-docx.

## Run locally
1. Create a virtual environment:
   `python -m venv .venv`
2. Activate it.
3. Install dependencies:
   `pip install -r requirements.txt`
4. Start:
   `uvicorn app.main:app --reload`
5. Open:
   `http://127.0.0.1:8000`

## Project structure
- `app/main.py` - API and application logic
- `app/static/index.html` - UI
- `app/static/styles.css` - dashboard styling
- `app/static/app.js` - browser logic

## Important
This project should be tested locally before being described as a completed portfolio project. Do not claim features you have not run and verified.
