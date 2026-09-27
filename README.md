# CareerLens AI

### AI-Powered Resume Intelligence & Job Matching

CareerLens AI is an AI-assisted web application that analyzes a candidate's resume against a target job description.

It combines semantic similarity analysis with technical skill matching to estimate how well a resume aligns with a particular job and provides actionable suggestions for improvement.

---

## 🚀 Features

- 📄 Upload resumes in PDF or DOCX format
- 📝 Enter a target job description
- 🔍 Extract readable resume text automatically
- 🛠️ Detect technical skills from resumes and job descriptions
- 🤖 Semantic resume-to-job similarity using Sentence Transformers
- 📊 Calculate an overall job-match score
- ✅ Identify matched skills
- ❌ Identify missing skills
- 💡 Generate actionable resume improvement suggestions
- 🌐 Simple web-based user interface

---

## 🧠 How CareerLens AI Works

CareerLens AI analyzes a resume and job description through multiple stages:

### 1. Resume Upload

The user uploads a resume in PDF or DOCX format.

### 2. Text Extraction

The application extracts readable text from the uploaded resume using:

- PyPDF
- python-docx

### 3. Skill Detection

CareerLens AI searches the resume and job description for technical skills such as:

- Python
- Java
- JavaScript
- SQL
- React
- FastAPI
- Machine Learning
- NLP
- Generative AI
- AWS
- Azure
- Docker
- Git
- TensorFlow
- PyTorch
- Pandas
- NumPy
- and many more

### 4. Semantic Similarity

Sentence Transformers are used to generate embeddings for the resume and job description.

Cosine similarity is then used to measure how semantically relevant the resume is to the job description.

### 5. Skill Coverage

The application compares the skills detected in the resume with the skills required by the job description.

It identifies:

- Matched skills
- Missing skills
- Overall skill coverage

### 6. Overall Match Score

CareerLens AI combines semantic relevance and skill coverage into a transparent weighted score:

```text
Overall Match =
(Semantic Similarity × 60%)
+
(Skill Coverage × 40%)