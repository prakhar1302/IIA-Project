import pdfplumber
import re
from typing import Dict

def extract_resume_info(pdf_path: str) -> Dict:
    """
    Extract relevant information from a PDF resume and return it as a dictionary.

    Args:
        pdf_path (str): Path to the PDF file

    Returns:
        Dict: Dictionary containing extracted resume information
    """
    resume_data = {
        'name': None,
        'email': None,
        'phone': None,
        'education': [],
        'experience': [],
        'skills': []
    }

    # Regular expressions for pattern matching
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'\b(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b'

    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ''
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + '\n'

            # Split text into lines for processing
            lines = full_text.split('\n')

            # Extract email
            emails = re.findall(email_pattern, full_text)
            if emails:
                resume_data['email'] = emails[0]

            # Extract phone number
            phones = re.findall(phone_pattern, full_text)
            if phones:
                resume_data['phone'] = phones[0]

            # Assume the first non-empty line contains the name
            for line in lines:
                if line.strip():
                    resume_data['name'] = line.strip()
                    break

            # Process sections
            education_section = experience_section = skills_section = False
            current_education, current_experience, current_skills = [], [], []

            for line in lines:
                line = line.strip()

                # Check for section headers
                if 'education' in line.lower() or 'academic' in line.lower():
                    education_section, experience_section, skills_section = True, False, False
                    continue
                elif 'experience' in line.lower() or 'employment' in line.lower():
                    education_section, experience_section, skills_section = False, True, False
                    continue
                elif 'skills' in line.lower() or 'technologies' in line.lower():
                    education_section, experience_section, skills_section = False, False, True
                    continue

                # Add content to the appropriate section
                if education_section:
                    current_education.append(line)
                elif experience_section:
                    current_experience.append(line)
                elif skills_section:
                    if ',' in line:
                        current_skills.extend([skill.strip() for skill in line.split(',')])
                    else:
                        current_skills.append(line)

            resume_data['education'] = current_education
            resume_data['experience'] = current_experience
            resume_data['skills'] = current_skills

    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        return None

    return resume_data
