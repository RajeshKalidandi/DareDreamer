from src.app import create_app, db
from src.models import User, Job, Application, Employer, InterviewSlot
from src.spiders.job_spider import JobSpider
from src.job_matcher import JobMatcher, load_jobs_from_db
import logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

app = create_app()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl(JobSpider)
    process.start()

def run_job_matcher():
    jobs = load_jobs_from_db()
    if jobs:
        matcher = JobMatcher()
        matcher.fit(jobs)
        return matcher
    else:
        logger.warning("No jobs available for matching. Please run the job spider first.")
        return None

def main():
    with app.app_context():
        db.create_all()

    # Run the spider to collect job data
    logger.info("Starting job spider...")
    run_spider()
    logger.info("Job spider completed.")

    # Initialize and run the job matcher
    logger.info("Initializing job matcher...")
    matcher = run_job_matcher()

    if matcher:
        # Example usage of the job matcher
        user_profile = input("Enter your job profile (skills, experience, etc.): ")
        matches = matcher.get_matches(user_profile)
        
        print(f"\nTop matches for your profile:")
        for i, match in enumerate(matches, 1):
            print(f"{i}. {match['title']} at {match['company']} - {match['location']}")
    else:
        logger.error("Job matcher initialization failed.")

if __name__ == "__main__":
    main()
