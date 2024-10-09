import scrapy
from src.models import Job
from src.database import insert_job
from datetime import datetime

class WellfoundSpider(scrapy.Spider):
    name = "wellfound"
    allowed_domains = ["wellfound.com"]
    
    def __init__(self, keywords='', location='', *args, **kwargs):
        super(WellfoundSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'https://wellfound.com/jobs?q={keywords}&l={location}']

    def parse(self, response):
        jobs = response.css('div.styles-module_jobCard__VeEZR')
        for job in jobs:
            title = job.css('h2.styles-module_title__Nv8Ov::text').get().strip()
            company = job.css('div.styles-module_company__Xj7Gu::text').get().strip()
            location = job.css('div.styles-module_location__Uy2Oi::text').get().strip()
            job_url = job.css('a::attr(href)').get()
            
            job_data = {
                'title': title,
                'company': company,
                'location': location,
                'url': response.urljoin(job_url),
                'date_posted': datetime.now(),
                'source': 'Wellfound'
            }
            insert_job(job_data)

        next_page = response.css('a[data-test="pagination-next"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)