from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from pdfToText import *
from api import *
import markdown

# from flaskext.markdown import Markdown

class Messg:
    def __init__(self, text) -> None:
        self.text = text

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

def enhanceResume(resume_text, user_name ,target_job):
    enhanced_resume = f"{resume_text}"
    user_message =  Messg(f"Enhanced this resume {enhanced_resume} which is  for {user_name} ,with the target job profile of {target_job}.")
    enhanced_resume = prompt.get_chat_response(user_message)
    return markdown.markdown(enhanced_resume)

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

        enhanced_resume = enhanceResume(resume_text, user_name, target_job)
        # Convert and save as PDF
        ##uploads/YashSharma_B20241.pdf
        new_file_path = resume_path.split('/')[-1]
        print(new_file_path)
        makepdf(enhanced_resume, new_file_path)

        return render_template('result.html', user_name=user_name, original_resume=resume_text, enhanced_resume=enhanced_resume)

    return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)
