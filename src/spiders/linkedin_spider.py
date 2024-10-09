import scrapy
from src.models import Job
from src.database import db, insert_job
from datetime import datetime

class LinkedInSpider(scrapy.Spider):
    name = "linkedin"
    allowed_domains = ["linkedin.com"]
    
    def __init__(self, keywords='', location='', *args, **kwargs):
        super(LinkedInSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'https://www.linkedin.com/jobs/search/?keywords={keywords}&location={location}']

    def parse(self, response):
        jobs = response.css('div.base-card')
        for job in jobs:
            title = job.css('h3.base-search-card__title::text').get().strip()
            company = job.css('h4.base-search-card__subtitle::text').get().strip()
            location = job.css('span.job-search-card__location::text').get().strip()
            job_url = job.css('a.base-card__full-link::attr(href)').get()
            
            job_data = {
                'title': title,
                'company': company,
                'location': location,
                'url': job_url,
                'date_posted': datetime.now(),
                'source': 'LinkedIn'
            }
            insert_job(job_data)

        next_page = response.css('a.next-page::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)