# coding: utf-8

import scrapy
import re
from restaurants.items import RestaurantsItem


class RestaurantSpider(scrapy.Spider):
    """This spider crawls restaurants.mu to retrieve restaurants data."""
    
    name = "restaurants"
    start_urls = [
        'http://restaurants.mu/search/?town=0&delivery=0&page=1',
    ]
    
    def parse(self, response):
        """Follows pagination links and iterates over restaurants listings."""
        # Item definition
        item = RestaurantsItem()
        # XPath for listings in the current page
        xpt_listing = '/'.join(
            ['//div[@id="listing"]',
             'div[contains(@class, "row listing listing")]',
             'div[@class="col info"]']
        )
        # Iterate through listings and extract and save items
        for listing in response.xpath(xpt_listing):
            item['title'] = listing.xpath('./h3/a/@title').extract_first()
            item['address'] = listing.xpath(
                './div[@class="address"]/text()'
            ).extract_first() 
            row = listing.xpath('./div[@class="row"]')
            item['cuisines'] = row.xpath('./div/div[@class="category"]/text()'
                                        ).extract()
            item['cuisines'] = self._cleanInput(''.join(item['cuisines']))
            item['opening'] = row.xpath('./div/div[@class="opening"]//text()'
                                       ).extract()
            item['opening'] = self._cleanInput(''.join(item['opening']))
            item['phone'] = row.xpath('./div/div[@class="phones"]//text()'
                                     ).extract()
            item['phone'] = self._cleanInput(''.join(item['phone']))
            yield item
        
        # Follow "Next" link
        xpt_next = '/'.join(
            ['//div[@id="snippet--content"]', 'div', 'div', 'div',
             'div[@class="paginator"]', 'a[contains(text(), "Next ")]',
             '@href']
        )
        next_page = response.xpath(xpt_next).extract_first()
        if next_page:
            # Takes numpage from urlref and inserts is into the url
            numpage = next_page.split('&')[0].split('=')[1]
            next_page = '?town=0&delivery=0&page={}'.format(numpage)
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback= self.parse,
                                dont_filter= True,
                                meta={'handle_http_status_list': [301]}
                                )

    def _cleanInput(self, strin):
        # Eliminate all breaklines
        strin = re.sub('\n', '', strin)
        # Remove all repeated spaces before/after text
        strin = re.sub('^[ ]+|[ ]+$', '', strin)
        # Remove double spaces between text or non-breakable isolatin spaces
        return re.sub(u'[ ]{2,}|\xa0', u' ', strin)
