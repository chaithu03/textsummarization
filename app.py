from flask import Flask, render_template, request
from transformers import pipeline
import pdfplumber
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # specify a folder for temporary PDF storage

# Initialize summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        patient_name = request.form['patient_name']
        doctor_name = request.form['doctor_name']
        date = request.form['date']
        text = request.form.get('text', '')

        # Check if a PDF file is uploaded
        if 'file' in request.files and request.files['file'].filename != '':
            pdf_file = request.files['file']
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
            pdf_file.save(pdf_path)

            # Extract text from PDF
            with pdfplumber.open(pdf_path) as pdf:
                text = '\n'.join([page.extract_text() for page in pdf.pages])

            os.remove(pdf_path)  # Delete file after extracting text

        # Generate summary if text is provided
        if text:
            summary = summarizer(text, max_length=250, min_length=70, do_sample=False)[0]['summary_text']
            return render_template('summary.html', patient_name=patient_name, doctor_name=doctor_name, date=date, summary=summary)

    return render_template('input_form.html')

if __name__ == '__main__':
    app.run(debug=True)
