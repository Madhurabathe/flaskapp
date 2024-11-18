from PyPDF2 import PdfReader
from docx import Document
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# text from PDF
def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# text from DOCX
def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text
    return text

#  email from text
def extract_email(text):
    email = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return email.group() if email else "Not Found"

# skills from text
def extract_skills(text, skill_set):
    skills_found = [skill for skill in skill_set if skill.lower() in text.lower()]
    return skills_found

# score
def calculate_similarity(resume_text, job_description):
    documents = [resume_text, job_description]
    vectorizer = CountVectorizer().fit_transform(documents)
    vectors = vectorizer.toarray()
    return cosine_similarity(vectors)[0, 1]
