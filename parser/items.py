# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParserItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    links = scrapy.Field()
