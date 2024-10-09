from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, current_app
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
import os
from .models import db, User, Application, Job  # Add Application and Job to the imports
from .resume_extractor import extract_resume_info
from .job_matcher import get_recent_matches, get_job_recommendations  # Import these functions
import json
from sqlalchemy import func, or_  # Import func and or_ for database queries
from datetime import datetime, timedelta
from src.tasks import run_spider, run_all_spiders
from src.spiders.linkedin_spider import LinkedInSpider
from src.spiders.naukri_spider import NaukriSpider
from src.spiders.glassdoor_spider import GlassdoorSpider
from src.spiders.wellfound_spider import WellfoundSpider
import threading

bp = Blueprint('main', __name__)

# Add all your route definitions here
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def run_spider(spider_class, keywords, location):
    process = CrawlerProcess(get_project_settings())
    process.crawl(spider_class, keywords=keywords, location=location)
    process.start()

def run_all_spiders():
    process = CrawlerProcess(get_project_settings())
    process.crawl(LinkedInSpider)
    process.crawl(NaukriSpider)
    process.crawl(GlassdoorSpider)
    process.crawl(WellfoundSpider)
    process.start()

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
                os.makedirs(uploads_dir, exist_ok=True)
                file_path = os.path.join(uploads_dir, filename)
                file.save(file_path)
                
                # Extract information from the resume
                extracted_info = extract_resume_info(file_path)
                
                # Update user profile with extracted information
                current_user.full_name = extracted_info.get('full_name', current_user.full_name)
                current_user.email = extracted_info.get('email', current_user.email)
                current_user.phone = extracted_info.get('phone', current_user.phone)
                current_user.skills = ', '.join(extracted_info.get('skills', []))
                current_user.set_experience(extracted_info.get('experience', []))
                current_user.set_education(extracted_info.get('education', []))
                current_user.summary = extracted_info.get('summary', current_user.summary)
                
                db.session.commit()
                flash('Resume information extracted and profile updated successfully.')
                
                # Remove the file after processing
                os.remove(file_path)
            else:
                flash('Invalid file format. Please upload a PDF or DOCX file.')
        else:
            flash('No file uploaded.')
    
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
        keywords = request.form.get('keywords', '')
        location = request.form.get('location', '')
        job_type = request.form.get('job_type', '')
        experience_level = request.form.get('experience_level', '')
        salary_range = request.form.get('salary_range', '')
        date_posted = request.form.get('date_posted', '')

        query = Job.query

        if keywords:
            query = query.filter(or_(
                Job.title.ilike(f'%{keywords}%'),
                Job.description.ilike(f'%{keywords}%'),
                Job.company.ilike(f'%{keywords}%')
            ))

        if location:
            query = query.filter(Job.location.ilike(f'%{location}%'))

        if job_type:
            query = query.filter(Job.job_type == job_type)

        if experience_level:
            query = query.filter(Job.experience_level == experience_level)

        if salary_range:
            min_salary, max_salary = map(int, salary_range.split('-'))
            query = query.filter(Job.salary.between(min_salary, max_salary))

        if date_posted:
            days = int(date_posted)
            date_threshold = datetime.utcnow() - timedelta(days=days)
            query = query.filter(Job.date_posted >= date_threshold)

        jobs = query.order_by(Job.date_posted.desc()).all()
        return render_template('search_results.html', jobs=jobs)

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

@bp.route('/scrape_jobs')
@login_required
def scrape_all_jobs():
    run_all_spiders()
    flash('Job scraping started for all sources. Please check back later for results.')
    return redirect(url_for('main.search'))

@bp.route('/scrape_jobs/<source>')
@login_required
def scrape_specific_jobs(source):
    keywords = request.args.get('keywords', '')
    location = request.args.get('location', '')
    
    spider_map = {
        'linkedin': LinkedInSpider,
        'naukri': NaukriSpider,
        'glassdoor': GlassdoorSpider,
        'wellfound': WellfoundSpider
    }
    
    if source in spider_map:
        run_spider(spider_map[source], keywords, location)
        flash(f'Job scraping from {source.capitalize()} started. Please check back later for results.')
    else:
        flash('Invalid job source selected.')
    
    return redirect(url_for('main.search'))

# Add other routes as needed