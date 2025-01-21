from scrapy.crawler import CrawlerRunner
from parser.spiders.advanced_spider import AdvancedSpider
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from scrapy.utils.log import configure_logging
import asyncio

async def run_spider():
    """Асинхронная функция для запуска паука"""
    configure_logging()
    runner = CrawlerRunner(settings=get_project_settings())
    deferred = runner.crawl(AdvancedSpider)
    deferred.addBoth(lambda _: reactor.stop())
    await asyncio.get_event_loop().run_in_executor(None, reactor.run, False)

