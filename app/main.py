from fastapi import FastAPI, File, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
from pypdf import PdfReader
from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import tempfile
import os


# ---------------------------------------------------------
# APP CONFIGURATION
# ---------------------------------------------------------

BASE = Path(__file__).resolve().parent

app = FastAPI(
    title="CareerLens AI",
    version="1.1.0"
)


# ---------------------------------------------------------
# STATIC FILES
# ---------------------------------------------------------

STATIC_DIR = BASE / "static"

if STATIC_DIR.exists():
    app.mount(
        "/static",
        StaticFiles(directory=str(STATIC_DIR)),
        name="static"
    )


# ---------------------------------------------------------
# SKILL DATABASE
# ---------------------------------------------------------

SKILLS = [
    "python",
    "java",
    "javascript",
    "typescript",
    "c",
    "c++",
    "c#",
    "sql",

    "html",
    "html5",
    "css",
    "css3",
    "react",
    "angular",
    "vue",
    "node.js",
    "express",
    "bootstrap",

    "django",
    "flask",
    "fastapi",
    "rest api",
    "graphql",

    "git",
    "github",
    "docker",
    "kubernetes",

    "aws",
    "azure",
    "gcp",

    "machine learning",
    "deep learning",
    "natural language processing",
    "nlp",
    "generative ai",
    "artificial intelligence",
    "llm",
    "openai",
    "gpt",
    "langchain",

    "tensorflow",
    "pytorch",
    "scikit-learn",
    "pandas",
    "numpy",
    "opencv",
    "spacy",
    "nltk",

    "postgresql",
    "mysql",
    "mongodb",
    "redis",
    "dbms",
    "database",

    "data analysis",
    "data science",
    "statistics",
    "power bi",
    "tableau",

    "linux",
    "spark",
    "hadoop",
    "streamlit",
    "flutter",
]


# ---------------------------------------------------------
# SKILL ALIASES
# ---------------------------------------------------------

ALIASES = {
    "html5": "html",
    "css3": "css",
    "natural language processing": "nlp",
    "artificial intelligence": "ai",
    "database management system": "dbms",
}


# ---------------------------------------------------------
# AI MODEL
# ---------------------------------------------------------




# ---------------------------------------------------------
# FILE TEXT EXTRACTION
# ---------------------------------------------------------

def extract_text(path: str) -> str:

    file_path = Path(path)
    extension = file_path.suffix.lower()

    if extension == ".pdf":

        reader = PdfReader(str(file_path))

        return "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    if extension == ".docx":

        document = Document(str(file_path))

        return "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        )

    raise ValueError(
        "Only PDF and DOCX files are supported."
    )


# ---------------------------------------------------------
# TEXT NORMALIZATION
# ---------------------------------------------------------

def normalize(text: str) -> str:

    text = text.lower()

    text = text.replace("•", " ")
    text = text.replace("–", "-")
    text = text.replace("—", "-")

    return re.sub(
        r"\s+",
        " ",
        text
    ).strip()


# ---------------------------------------------------------
# SKILL DETECTION
# ---------------------------------------------------------

def skill_exists(
    text: str,
    skill: str
) -> bool:

    text = normalize(text)
    skill = skill.lower()

    pattern = (
        r"(?<![a-z0-9])"
        + re.escape(skill)
        + r"(?![a-z0-9])"
    )

    return (
        re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )
        is not None
    )


def find_skills(text: str) -> list[str]:

    found = set()

    for skill in SKILLS:

        if skill_exists(
            text,
            skill
        ):

            found.add(
                ALIASES.get(
                    skill,
                    skill
                )
            )

    return sorted(found)


# ---------------------------------------------------------
# SEMANTIC SIMILARITY
# ---------------------------------------------------------

def semantic_score(resume: str, job: str) -> float:
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=5000
    )

    vectors = vectorizer.fit_transform([
        normalize(resume)[:12000],
        normalize(job)[:12000]
    ])

    similarity = float(
        cosine_similarity(
            vectors[0:1],
            vectors[1:2]
        )[0][0]
    )

    return max(0.0, min(1.0, similarity))

# ---------------------------------------------------------
# BUILD ANALYSIS
# ---------------------------------------------------------

def build_analysis(
    resume: str,
    job: str
) -> dict:

    resume_skills = set(
        find_skills(resume)
    )

    job_skills = set(
        find_skills(job)
    )

    matched_skills = sorted(
        resume_skills &
        job_skills
    )

    missing_skills = sorted(
        job_skills -
        resume_skills
    )

    semantic = semantic_score(
        resume,
        job
    )

    if job_skills:

        skill_coverage = (
            len(matched_skills)
            /
            len(job_skills)
        )

    else:

        skill_coverage = 0.0

    score = round(
        (
            semantic * 0.60
            +
            skill_coverage * 0.40
        )
        * 100
    )

    score = max(
        0,
        min(
            100,
            score
        )
    )


    # -----------------------------------------------------
    # RECOMMENDATIONS
    # -----------------------------------------------------

    recommendations = []

    if missing_skills:

        recommendations.append(
            "Consider learning or demonstrating: "
            + ", ".join(
                missing_skills[:8]
            )
            + "."
        )

    if score < 60:

        recommendations.append(
            "Tailor your professional summary "
            "and project descriptions to the "
            "main requirements of the job."
        )

    if not re.search(
        r"\b(project|projects|developed|built|"
        r"implemented|created)\b",
        normalize(resume)
    ):

        recommendations.append(
            "Add concrete projects with "
            "technologies used, your contribution, "
            "and measurable results."
        )

    if not re.search(
        r"\b(github|linkedin)\b",
        normalize(resume)
    ):

        recommendations.append(
            "Include your GitHub and LinkedIn "
            "profiles in the resume header."
        )

    if not recommendations:

        recommendations.append(
            "Strong alignment. Keep the resume "
            "focused on the requirements that "
            "appear most frequently in the job description."
        )


    return {

        "score": score,

        "semantic_similarity": round(
            semantic * 100,
            1
        ),

        "skill_coverage": round(
            skill_coverage * 100,
            1
        ),

        "resume_skills": sorted(
            resume_skills
        ),

        "job_skills": sorted(
            job_skills
        ),

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "suggestions": recommendations
    }


# ---------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------

@app.get("/")
def home():

    index_file = (
        BASE /
        "static" /
        "index.html"
    )

    if not index_file.exists():

        return JSONResponse(
            {
                "error":
                "static/index.html was not found."
            },
            status_code=500
        )

    return FileResponse(
        index_file
    )


# ---------------------------------------------------------
# ANALYZE API
# ---------------------------------------------------------

@app.post("/api/analyze")
async def analyze(

    resume: UploadFile = File(...),

    job_description: str = Form(...)
):

    extension = Path(
        resume.filename or ""
    ).suffix.lower()


    # Validate resume
    if extension not in {
        ".pdf",
        ".docx"
    }:

        return JSONResponse(
            {
                "error":
                "Upload a PDF or DOCX resume."
            },
            status_code=400
        )


    # Validate job description
    if not job_description.strip():

        return JSONResponse(
            {
                "error":
                "Enter a job description."
            },
            status_code=400
        )


    file_data = await resume.read()

    temp_path = None


    try:

        # Create temporary file
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension
        ) as temp_file:

            temp_file.write(
                file_data
            )

            temp_path = temp_file.name


        # Extract resume text
        resume_text = extract_text(
            temp_path
        )


        # -------------------------------------------------
        # DEBUG OUTPUT
        # -------------------------------------------------

        print(
            "\n========== EXTRACTED RESUME TEXT =========="
        )

        print(resume_text)

        print(
            "============================================\n"
        )


        # Also show detected skills
        detected_skills = find_skills(
            resume_text
        )

        print(
            "========== DETECTED RESUME SKILLS =========="
        )

        print(
            detected_skills
        )

        print(
            "============================================\n"
        )


        # Check extracted text
        if len(
            resume_text.strip()
        ) < 50:

            return JSONResponse(
                {
                    "error":
                    "Not enough readable text "
                    "was found in the resume."
                },
                status_code=400
            )


        # Analyze
        result = build_analysis(
            resume_text,
            job_description
        )


        result[
            "resume_name"
        ] = resume.filename


        return result


    except Exception as error:

        return JSONResponse(
            {
                "error":
                f"Analysis failed: {error}"
            },
            status_code=500
        )


    finally:

        if temp_path:

            try:

                os.unlink(
                    temp_path
                )

            except OSError:

                pass