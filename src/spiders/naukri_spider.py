import scrapy
from src.models import Job
from src.database import db, insert_job
from datetime import datetime

class NaukriSpider(scrapy.Spider):
    name = "naukri"
    allowed_domains = ["naukri.com"]
    
    def __init__(self, keywords='', location='', *args, **kwargs):
        super(NaukriSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'https://www.naukri.com/jobs-in-{location}?k={keywords}']

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'ROBOTSTXT_OBEY': True,
        'DOWNLOAD_DELAY': 2,
    }

    def parse(self, response):
        jobs = response.css('article.jobTuple')
        for job in jobs:
            title = job.css('a.title::text').get().strip()
            company = job.css('a.subTitle::text').get().strip()
            location = job.css('li.location::text').get().strip()
            job_url = job.css('a.title::attr(href)').get()
            
            job_data = {
                'title': title,
                'company': company,
                'location': location,
                'url': job_url,
                'date_posted': datetime.now(),
                'source': 'Naukri'
            }
            insert_job(job_data)

        next_page = response.css('a.fright::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)