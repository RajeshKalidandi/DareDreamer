from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, current_app
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
import os
from .models import db, User, Application, Job  # Add Application and Job to the imports
from .resume_extractor import extract_resume_info
from .job_matcher import get_recent_matches, get_job_recommendations  # Import these functions
import json
from sqlalchemy import func  # Import func for database queries

bp = Blueprint('main', __name__)

# Add all your route definitions here
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.profile'))
        flash('Invalid username or password')
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        if 'resume' in request.files:
            file = request.files['resume']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                uploads_dir = os.path.join(current_app.root_path, 'uploads')
                os.makedirs(uploads_dir, exist_ok=True)  # This line ensures the uploads directory exists
                file_path = os.path.join(uploads_dir, filename)
                file.save(file_path)
                
                # Extract information from the resume
                extracted_info = extract_resume_info(file_path)
                
                # Update user profile with extracted information
                current_user.full_name = extracted_info.get('full_name', current_user.full_name)
                current_user.email = extracted_info.get('email', current_user.email)
                current_user.phone = extracted_info.get('phone', current_user.phone)
                current_user.skills = ', '.join(extracted_info.get('skills', []))
                current_user.experience = extracted_info.get('experience', [])
                current_user.education = extracted_info.get('education', [])
                current_user.summary = extracted_info.get('summary', current_user.summary)
                
                db.session.commit()
                flash('Resume information extracted and profile updated successfully.')
                
                # Remove the file after processing
                os.remove(file_path)
            else:
                flash('Invalid file format. Please upload a PDF or DOCX file.')
        else:
            flash('No file uploaded.')
    
    # Ensure experience and education are lists of dictionaries
    if isinstance(current_user.experience, str):
        current_user.experience = json.loads(current_user.experience)
    if isinstance(current_user.education, str):
        current_user.education = json.loads(current_user.education)
    
    return render_template('profile.html', user=current_user)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')
            return redirect(url_for('main.register'))
        
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful. Please log in.')
        return redirect(url_for('main.login'))
    
    return render_template('register.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    total_applications = Application.query.filter_by(user_id=current_user.id).count()
    application_stats = db.session.query(
        Application.status, func.count(Application.id)
    ).filter_by(user_id=current_user.id).group_by(Application.status).all()
    application_stats = dict(application_stats)

    # Get recent job matches (you'll need to implement this function)
    recent_matches = get_recent_matches(current_user)

    # Get upcoming interviews
    upcoming_interviews = Application.query.filter_by(
        user_id=current_user.id, 
        status='Interviewing'
    ).order_by(Application.applied_date.desc()).limit(5).all()

    # Get job recommendations (you'll need to implement this function)
    similar_jobs = get_job_recommendations(current_user)

    return render_template('dashboard.html', 
                           total_applications=total_applications,
                           application_stats=application_stats,
                           recent_matches=recent_matches,
                           upcoming_interviews=upcoming_interviews,
                           similar_jobs=similar_jobs)

@bp.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        # Implement your search logic here
        # For now, let's return an empty list
        return jsonify([])
    return render_template('search.html')

@bp.route('/applications')
@login_required
def applications():
    # Add applications logic here
    return render_template('applications.html')

@bp.route('/recommendations')
@login_required
def recommendations():
    # Add recommendations logic here
    return render_template('recommendations.html')

@bp.route('/employer/register', methods=['GET', 'POST'])
@login_required
def employer_register():
    # Add employer registration logic here
    return render_template('employer_register.html')

@bp.route('/employer/dashboard')
@login_required
def employer_dashboard():
    # Add employer dashboard logic here
    return render_template('employer_dashboard.html')

@bp.route('/employer/post_job', methods=['GET', 'POST'])
@login_required
def post_job():
    # Add job posting logic here
    return render_template('post_job.html')

# Add other routes as needed