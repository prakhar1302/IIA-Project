import pdfplumber
import re
from typing import Dict, Optional

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
                full_text += page.extract_text() + '\n'

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

            # Assume the first line contains the name
            if lines:
                resume_data['name'] = lines[0].strip()

            # Process education information
            education_section = False
            current_education = []

            # Process experience information
            experience_section = False
            current_experience = []

            # Process skills information
            skills_section = False
            current_skills = []

            for line in lines:
                line = line.strip()

                # Skip empty lines
                if not line:
                    continue

                # Check for section headers
                if any(keyword in line.lower() for keyword in ['education', 'academic']):
                    education_section = True
                    experience_section = False
                    skills_section = False
                    continue

                elif any(keyword in line.lower() for keyword in ['experience', 'employment', 'work history']):
                    education_section = False
                    experience_section = True
                    skills_section = False
                    continue

                elif any(keyword in line.lower() for keyword in ['skills', 'technologies', 'competencies']):
                    education_section = False
                    experience_section = False
                    skills_section = True
                    continue

                # Add content to appropriate sections
                if education_section:
                    current_education.append(line)
                elif experience_section:
                    current_experience.append(line)
                elif skills_section:
                    # Split skills by commas if present
                    if ',' in line:
                        current_skills.extend([skill.strip() for skill in line.split(',')])
                    else:
                        current_skills.append(line)

            # Add processed sections to resume_data
            resume_data['education'] = current_education
            resume_data['experience'] = current_experience
            resume_data['skills'] = current_skills

    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        return None

    return resume_data

def print_resume_info(resume_data: Dict) -> None:
    """
    Print the extracted resume information in a formatted way.

    Args:
        resume_data (Dict): Dictionary containing resume information
    """
    if resume_data:
        print("\n=== RESUME INFORMATION ===\n")
        print(f"Name: {resume_data['name']}")
        print(f"Email: {resume_data['email']}")
        print(f"Phone: {resume_data['phone']}")

        print("\nEducation:")
        for edu in resume_data['education']:
            print(f"- {edu}")

        print("\nExperience:")
        for exp in resume_data['experience']:
            print(f"- {exp}")

        print("\nSkills:")
        for skill in resume_data['skills']:
            print(f"- {skill}")
    else:
        print("No resume data available.")

# # Example usage
# if __name__ == "__main__":
#     pdf_path = "path/to/your/resume.pdf"  # Update with the actual path
#     resume_info = extract_resume_info(pdf_path)
#     print_resume_info(resume_info)
#     print("\n=== END OF INFORMATION ===\n")
#     print(resume_info['skills'])
