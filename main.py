from scrapy.crawler import CrawlerProcess
from parser.spiders.advanced_spider import AdvancedSpider
from scrapy.utils.project import get_project_settings

import logging

def run_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl(AdvancedSpider)
    process.start()


if __name__ == "__main__":
    run_spider()
