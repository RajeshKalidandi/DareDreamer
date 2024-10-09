from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_connection():
    # This function is no longer needed, but we'll keep it for now to avoid breaking other parts of the code
    return db

def insert_job(job_data):
    # Update this function to use SQLAlchemy
    from src.models import Job  # Import here to avoid circular imports
    new_job = Job(**job_data)
    db.session.add(new_job)
    db.session.commit()
    return new_job.id

# Remove or comment out other functions that are no longer needed