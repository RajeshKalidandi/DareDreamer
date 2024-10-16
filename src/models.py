from .database import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    
    # Enhanced profile fields
    full_name = db.Column(db.String(100))
    headline = db.Column(db.String(200))
    summary = db.Column(db.Text)
    skills = db.Column(db.Text)  # Comma-separated list of skills
    experience = db.Column(db.Text)  # JSON string of work experience
    education = db.Column(db.Text)  # JSON string of education history
    location = db.Column(db.String(100))
    desired_job_title = db.Column(db.String(100))
    phone = db.Column(db.String(20))

    # Relationship with applications
    applications = db.relationship('Application', backref='applicant', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_experience(self, experience_list):
        self.experience = json.dumps(experience_list)

    def get_experience(self):
        return json.loads(self.experience) if self.experience else []

    def set_education(self, education_list):
        self.education = json.dumps(education_list)

    def get_education(self):
        return json.loads(self.education) if self.education else []

class Employer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.Text)
    website = db.Column(db.String(200))
    
    user = db.relationship('User', backref='employer', uselist=False)
    jobs = db.relationship('Job', backref='employer', lazy=True)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    url = db.Column(db.String(500))
    description = db.Column(db.Text)
    salary = db.Column(db.String(50))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    job_type = db.Column(db.String(50))
    experience_level = db.Column(db.String(50))
    employer_id = db.Column(db.Integer, db.ForeignKey('employer.id'), nullable=True)
    source = db.Column(db.String(50))  # Add this line

    applications = db.relationship('Application', backref='job', lazy=True)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    status = db.Column(db.String(20), default='Applied')  # Applied, Interviewing, Offered, Rejected
    applied_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    interview_slot_id = db.Column(db.Integer, db.ForeignKey('interview_slot.id'))

    interview_slot = db.relationship('InterviewSlot', backref='application', uselist=False)

class InterviewSlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    is_available = db.Column(db.Boolean, default=True)

    job = db.relationship('Job', backref='interview_slots')