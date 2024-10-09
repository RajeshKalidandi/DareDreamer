# Dare Dreamer Job Search Platform

## Project Overview

Dare Dreamer is an advanced job search platform that combines web scraping, machine learning, and user-friendly interfaces to help job seekers find their dream positions. The platform scrapes job listings from multiple sources, provides personalized job recommendations, and offers tools for managing applications and interviews.

## Key Features

- User authentication and profile management
- Resume parsing and information extraction
- Job scraping from multiple sources (LinkedIn, Naukri, Glassdoor, Wellfound)
- Advanced job search functionality
- Personalized job recommendations
- Application tracking
- Interview scheduling (for both job seekers and employers)
- Employer dashboard for posting jobs and managing applications

## Technology Stack

- Backend: Python, Flask
- Database: SQLAlchemy with SQLite (can be easily switched to PostgreSQL for production)
- Web Scraping: Scrapy
- Machine Learning: NLTK, scikit-learn
- Frontend: HTML, CSS (Bootstrap), JavaScript

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/daredreamer.git
   cd daredreamer
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the project root and add the following:
   ```bash
   FLASK_APP=src.wsgi:app
   FLASK_ENV=development
   SECRET_KEY=your_secret_key_here
   DATABASE_URL=sqlite:///job_search.db
   ```

5. Set up the database:
   ```bash
   flask db upgrade
   ```

6. Run the application:
   ```bash
   flask run
   ```

## Usage

1. Register as a user or employer
2. Upload your resume to populate your profile
3. Search for jobs or post new job listings (as an employer)
4. Apply for jobs and manage your applications
5. Schedule interviews and track your job search progress

## Development Progress

- [x] Basic project structure and database models
- [x] User authentication and profile management
- [x] Resume parsing and information extraction
- [x] Job scraping from LinkedIn
- [x] Basic job search functionality
- [ ] Implement job scraping for Naukri, Glassdoor, and Wellfound
- [ ] Enhance job matching algorithm
- [ ] Implement application tracking system
- [ ] Develop interview scheduling feature
- [ ] Create employer dashboard
- [ ] Improve UI/UX design
- [ ] Implement email notifications
- [ ] Add data visualization for job search statistics

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
