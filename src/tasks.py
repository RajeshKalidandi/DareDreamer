from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from src.spiders.linkedin_spider import LinkedInSpider
from src.spiders.naukri_spider import NaukriSpider
from src.spiders.glassdoor_spider import GlassdoorSpider
from src.spiders.wellfound_spider import WellfoundSpider
import threading

def run_spider(spider_class, keywords, location):
    def crawl():
        process = CrawlerProcess(get_project_settings())
        process.crawl(spider_class, keywords=keywords, location=location)
        process.start()
    
    thread = threading.Thread(target=crawl)
    thread.start()

def run_all_spiders():
    def crawl_all():
        process = CrawlerProcess(get_project_settings())
        process.crawl(LinkedInSpider)
        process.crawl(NaukriSpider)
        process.crawl(GlassdoorSpider)
        process.crawl(WellfoundSpider)
        process.start()
    
    thread = threading.Thread(target=crawl_all)
    thread.start()