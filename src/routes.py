from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from src.models import db, User, Job, Application, Employer, InterviewSlot
from src.job_matcher import JobMatcher
import logging
import json
from datetime import datetime, timedelta
from sqlalchemy import func

bp = Blueprint('main', __name__)

# Add all your route definitions here
@bp.route('/')
def home():
    return render_template('home.html')

# ... (add all other routes from app.py)