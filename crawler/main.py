from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from .spiders import GHE, TeamAPI


def start():
    process = CrawlerProcess(get_project_settings())
    process.crawl(GHE)
    process.crawl(TeamAPI)
    process.start() # the script will block here until all crawling jobs are finished
