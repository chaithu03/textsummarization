from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)

# Initialize the summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        patient_name = request.form['patient_name']
        doctor_name = request.form['doctor_name']
        date = request.form['date']
        text = request.form['text']
        
        # Adjust the summarization parameters for a more detailed summary
        summary = summarizer(text, max_length=250, min_length=100, do_sample=False)[0]['summary_text']
        
        return render_template('summary.html', patient_name=patient_name, doctor_name=doctor_name, date=date, summary=summary)
    return render_template('input_form.html')

if __name__ == '__main__':
    app.run(debug=True)
