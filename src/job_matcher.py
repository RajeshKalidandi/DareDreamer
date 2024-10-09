import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
from .models import Job  # Import Job model
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Download necessary NLTK data
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

class JobMatcher:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'))
        self.job_vectors = None
        self.jobs = None

    def preprocess_job(self, job):
        return f"{job.title} {job.company} {job.location} {job.description} {job.requirements}"

    def preprocess_user(self, user):
        experience = json.loads(user.experience) if user.experience else []
        education = json.loads(user.education) if user.education else []
        
        experience_text = " ".join([f"{exp['title']} {exp['company']} {exp['description']}" for exp in experience])
        education_text = " ".join([f"{edu['degree']} {edu['institution']} {edu['field_of_study']}" for edu in education])
        
        return f"{user.full_name} {user.headline} {user.summary} {user.skills} {experience_text} {education_text} {user.location} {user.desired_job_title}"

    def fit(self, jobs):
        self.jobs = jobs
        job_texts = [self.preprocess_job(job) for job in jobs]
        self.job_vectors = self.vectorizer.fit_transform(job_texts)

    def get_matches(self, user, top_n=5):
        user_text = self.preprocess_user(user)
        user_vector = self.vectorizer.transform([user_text])
        similarities = cosine_similarity(user_vector, self.job_vectors)
        top_indices = similarities.argsort()[0][-top_n:][::-1]
        return [self.jobs[i] for i in top_indices]

def get_recent_matches(user, limit=5):
    # Implement logic to get recent job matches for the user
    # For now, return an empty list
    return []

def get_job_recommendations(user, limit=3):
    # Implement logic to get job recommendations for the user
    # For now, return an empty list
    return []

# Remove the if __name__ == "__main__" block as it's not needed here