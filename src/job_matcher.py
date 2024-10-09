import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
from src.database import create_connection, get_all_jobs
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

    def get_similar_jobs(self, job_ids, top_n=5):
        if not self.jobs or not self.job_vectors:
            return []

        applied_jobs = [job for job in self.jobs if job['id'] in job_ids]
        applied_job_texts = [self.preprocess_job(job) for job in applied_jobs]
        applied_vectors = self.vectorizer.transform(applied_job_texts)

        avg_vector = applied_vectors.mean(axis=0)
        similarities = cosine_similarity(avg_vector, self.job_vectors)
        top_indices = similarities.argsort()[0][-top_n-len(job_ids):][::-1]
        
        similar_jobs = [self.jobs[i] for i in top_indices if self.jobs[i]['id'] not in job_ids]
        return similar_jobs[:top_n]

def load_jobs_from_db():
    conn = create_connection()
    if conn is not None:
        jobs = get_all_jobs(conn)
        conn.close()
        return [dict(zip(['id', 'title', 'company', 'location', 'url', 'description', 'salary', 'date_posted', 'date_scraped'], job)) for job in jobs]
    else:
        logger.error("Unable to connect to the database")
        return []

if __name__ == "__main__":
    # Load jobs from the database
    jobs = load_jobs_from_db()

    if jobs:
        # Initialize and fit the job matcher
        matcher = JobMatcher()
        matcher.fit(jobs)

        # Example usage
        user_profile = "Experienced Python developer with machine learning skills"
        matches = matcher.get_matches(user_profile)
        
        print(f"Top matches for the user profile '{user_profile}':")
        for i, match in enumerate(matches, 1):
            print(f"{i}. {match['title']} at {match['company']} - {match['location']}")
    else:
        print("No jobs available for matching. Please run the job spider first to populate the database.")