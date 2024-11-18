from flask import Flask, request, render_template, redirect, url_for
import os
from utils import extract_text_from_pdf, extract_text_from_docx, extract_email, extract_skills, calculate_similarity

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Skills set
SKILL_SET = {"Python", "SQL", "Machine Learning", "Java"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Parsing the resume
        if file.filename.endswith('.pdf'):
            text = extract_text_from_pdf(filepath)
        elif file.filename.endswith('.docx'):
            text = extract_text_from_docx(filepath)

        # Extraction
        email = extract_email(text)
        skills = extract_skills(text, SKILL_SET)

        # Job description 
        job_description = "Expert java developer and great in machine learning efficient use of python and sql."
        # Calculate score
        match_score = calculate_similarity(text,job_description)

        return render_template('results.html', email=email, skills=skills, score=round(match_score * 100, 2))
    else:
        return "Invalid file format", 400

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
