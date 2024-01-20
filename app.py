from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from pdfToText import *
from api import *
# from flaskext.markdown import Markdown

app = Flask(__name__)
# Markdown(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

prompt = promptLLM()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def perform_ocr(pdf_path):
    return pdfToText(pdf_path).convertit()

def enhance_resume(resume_text, target_job):
    enhanced_resume = f"{resume_text}\n\nTarget Job: {target_job}"
    enhanced_resume = prompt.prompt(f"Give an enhanced resume with job title target job {target_job} and resume {enhance_resume}")
    return enhanced_resume

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'resume' not in request.files:
        return redirect(request.url)

    resume_file = request.files['resume']

    if resume_file.filename == '':
        return redirect(request.url)

    if resume_file and allowed_file(resume_file.filename):
        filename = secure_filename(resume_file.filename)
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        resume_file.save(resume_path)

        resume_text = perform_ocr(resume_path)

        user_name = request.form['user_name']
        target_job = request.form['target_job']

        enhanced_resume = enhance_resume(resume_text, target_job)

        return render_template('result.html', user_name=user_name, original_resume=resume_text, enhanced_resume=enhanced_resume)

    return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)
