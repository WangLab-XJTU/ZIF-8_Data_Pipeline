# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PaperItem(scrapy.Item):

    doi = scrapy.Field()
    file_name = scrapy.Field()
    file_type = scrapy.Field()
    status = scrapy.Field()
