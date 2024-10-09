import scrapy
from src.models import Job
from src.database import insert_job
from datetime import datetime

class GlassdoorSpider(scrapy.Spider):
    name = "glassdoor"
    allowed_domains = ["glassdoor.com"]
    
    def __init__(self, keywords='', location='', *args, **kwargs):
        super(GlassdoorSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'https://www.glassdoor.com/Job/jobs.htm?sc.keyword={keywords}&locT=C&locId={location}']

    def parse(self, response):
        jobs = response.css('li.react-job-listing')
        for job in jobs:
            title = job.css('a.jobLink::text').get().strip()
            company = job.css('div.employerName::text').get().strip()
            location = job.css('span.loc::text').get().strip()
            job_url = job.css('a.jobLink::attr(href)').get()
            
            job_data = {
                'title': title,
                'company': company,
                'location': location,
                'url': response.urljoin(job_url),
                'date_posted': datetime.now(),
                'source': 'Glassdoor'
            }
            insert_job(job_data)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)