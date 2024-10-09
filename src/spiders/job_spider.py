import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags
from src.database import create_connection, insert_job

class JobItem(scrapy.Item):
    title = scrapy.Field()
    company = scrapy.Field()
    location = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()
    salary = scrapy.Field()
    date_posted = scrapy.Field()

class JobSpider(scrapy.Spider):
    name = "jobs"
    allowed_domains = ["linkedin.com"]
    start_urls = [
        'https://www.linkedin.com/jobs/search/',
    ]

    custom_settings = {
        'USER_AGENT': 'DareDreamer JobBot (+https://www.daredreamer.com)',
        'ROBOTSTXT_OBEY': True,
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_DELAY': 1,
    }

    def __init__(self, *args, **kwargs):
        super(JobSpider, self).__init__(*args, **kwargs)
        self.db_conn = create_connection()

    def parse(self, response):
        for job in response.css('div.base-card'):
            loader = ItemLoader(item=JobItem(), selector=job)
            loader.default_output_processor = TakeFirst()

            loader.add_css('title', 'h3.base-search-card__title::text', MapCompose(str.strip))
            loader.add_css('company', 'h4.base-search-card__subtitle::text', MapCompose(str.strip))
            loader.add_css('location', 'span.job-search-card__location::text', MapCompose(str.strip))
            loader.add_css('url', 'a.base-card__full-link::attr(href)')
            loader.add_css('description', 'p.base-search-card__metadata::text', MapCompose(remove_tags, str.strip))
            loader.add_css('date_posted', 'time::attr(datetime)')

            job_item = loader.load_item()
            yield job_item

            # Insert job into database
            if self.db_conn:
                insert_job(self.db_conn, dict(job_item))

        next_page = response.css('a.next-page::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def closed(self, reason):
        if self.db_conn:
            self.db_conn.close()

    def parse_job_details(self, response):
        # Implement this method to scrape detailed job information if needed
        pass