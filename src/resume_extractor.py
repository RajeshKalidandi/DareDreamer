import re
import PyPDF2
import docx
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Download necessary NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

def extract_resume_info(file_path):
    if file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format")
    
    info = {
        'full_name': extract_name(text),
        'email': extract_email(text),
        'phone': extract_phone(text),
        'skills': extract_skills(text),
        'experience': extract_experience(text),
        'education': extract_education(text),
        'summary': extract_summary(text),
    }
    
    return info

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        text = ""
        for page in range(reader.getNumPages()):
            text += reader.getPage(page).extractText()
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return " ".join([para.text for para in doc.paragraphs])

def extract_name(text):
    # Assume the name is at the beginning of the resume
    lines = text.split('\n')
    for line in lines[:5]:  # Check first 5 lines
        if re.match(r'^[A-Z][a-z]+(?: [A-Z][a-z]+)+$', line.strip()):
            return line.strip()
    return ""

def extract_email(text):
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    matches = email_pattern.findall(text)
    return matches[0] if matches else ""

def extract_phone(text):
    phone_pattern = re.compile(r'\b(?:\+\d{1,2}\s?)?(?:\(\d{3}\)|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}\b')
    matches = phone_pattern.findall(text)
    return matches[0] if matches else ""

def extract_skills(text):
    skill_keywords = set(['python', 'java', 'c++', 'javascript', 'html', 'css', 'sql', 'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring', 'aws', 'azure', 'docker', 'kubernetes', 'git', 'agile', 'scrum'])
    words = text.lower().split()
    skills = list(set(words) & skill_keywords)
    return skills

def extract_experience(text):
    experience_pattern = re.compile(r'(?:experience|work history|employment).*?(?:education|skills|references|\Z)', re.DOTALL | re.IGNORECASE)
    match = experience_pattern.search(text)
    if match:
        experience_text = match.group()
        jobs = re.split(r'\n\n+', experience_text)
        experiences = []
        for job in jobs[1:]:  # Skip the "Experience" header
            lines = job.split('\n')
            if len(lines) >= 2:
                experiences.append({
                    'title': lines[0].strip(),
                    'company': lines[1].strip(),
                    'description': ' '.join(lines[2:]).strip()
                })
        return experiences
    return []

def extract_education(text):
    education_pattern = re.compile(r'(?:education|academic background).*?(?:experience|skills|references|\Z)', re.DOTALL | re.IGNORECASE)
    match = education_pattern.search(text)
    if match:
        education_text = match.group()
        schools = re.split(r'\n\n+', education_text)
        educations = []
        for school in schools[1:]:  # Skip the "Education" header
            lines = school.split('\n')
            if len(lines) >= 2:
                educations.append({
                    'degree': lines[0].strip(),
                    'institution': lines[1].strip(),
                    'graduation_date': lines[2].strip() if len(lines) > 2 else ''
                })
        return educations
    return []

def extract_summary(text):
    summary_pattern = re.compile(r'(?:summary|objective|profile).*?(?:experience|skills|education|\Z)', re.DOTALL | re.IGNORECASE)
    match = summary_pattern.search(text)
    if match:
        summary_text = match.group()
        sentences = summary_text.split('.')
        return '. '.join(sentences[:2])  # Return the first two sentences
    return ""