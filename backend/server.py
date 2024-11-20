from flask import Flask, request, jsonify, render_template
from extract_keywords import extract_resume_info
import os
from werkzeug.utils import secure_filename
from together import Together



app = Flask(__name__)
UPLOAD_FOLDER = 'C:\\Users\\ashar\\OneDrive\\Desktop\\3rd sem\\IIA\\IIA-Project\\backend\\upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the UPLOAD_FOLDER exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['resume']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Invalid file type, only PDFs are allowed'}), 400

    # Generate a fixed filename (e.g., 'resume.pdf' or the original filename)
    original_filename = secure_filename(file.filename)
    filename = "resume_" + original_filename  # You can change the naming convention as needed
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Delete the existing file if it already exists
    if os.path.exists(file_path):
        os.remove(file_path)

    # Save the uploaded file
    file.save(file_path)

    # Extract keywords from the resume
    resume_info = extract_resume_info(file_path)
    #print(resume_info)
    client = Together(api_key="60ed3ce132d7f1d7f4671e21785561eb98e08b6a43f69f12c44b7b8b8fb4e483")
    query = f"Give me the top 5 skills (no descriptions, just the skill names) from this skill set, separated by commas, and a boolean value indicating if the person is a fresher or not: Skills: {resume_info['skills']}, Experience: {'True' if resume_info['experience'] else 'False'}"

    print(resume_info['skills'])
    stream = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        messages=[{"role": "user", "content": query}],
        stream=True,
    )

    response_content = ""
    for chunk in stream:
        response_content += chunk.choices[0].delta.content or ""
    print(response_content)
    return jsonify({
        'analysis': response_content
    })

if __name__ == '__main__':
    app.run(debug=True)
