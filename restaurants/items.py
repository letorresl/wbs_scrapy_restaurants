# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RestaurantsItem(scrapy.Item):
    title = scrapy.Field()
    address = scrapy.Field()
    cuisines = scrapy.Field()
    opening = scrapy.Field()
    phone = scrapy.Field()
    website = scrapy.Field()
