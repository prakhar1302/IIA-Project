from flask import Flask, request, jsonify
from extract_keywords import extract_resume_info
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'C:\\Users\\pss13\\OneDrive\\Documents\\IIA\\IIA-Project\\uploads'

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['resume']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Save the uploaded file temporarily
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Extract keywords from resume
    resume_info = extract_resume_info(file_path)

    # Remove the file after processing
    os.remove(file_path)

    return jsonify({'keywords': resume_info['skills']})

if __name__ == '__main__':
    app.run(debug=True)
