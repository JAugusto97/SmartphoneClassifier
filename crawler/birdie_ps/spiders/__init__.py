# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
import pandas as pd

class SmartphoneSpider(scrapy.Spider):
    name = 'smartphone_spider'
    start_urls = ['https://www.submarino.com.br/categoria/celulares-e-smartphones/smartphone']
    data = pd.DataFrame(columns=['url', 'smartphone'])
    total_scrapped = data.shape[0]

    def parse(self, response):

        SET_SELECTOR = '.hUksZj'

        for smartphone in response.css(SET_SELECTOR):
            NAME_SELECTOR = '.YHJwU ::text'
            new_smartphone = smartphone.css(NAME_SELECTOR).extract_first()
            yield {
                'name':new_smartphone
            }

            self.data.loc[self.total_scrapped, 'url'] = response.request.url
            self.data.loc[self.total_scrapped, 'smartphone'] = new_smartphone
            self.total_scrapped += 1

        NEXT_PAGE_SELECTOR = '#content-middle li:nth-child(10) a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        else:
            print(self.total_scrapped)
            self.data.to_csv('/Users/joao/Desktop/SmartphoneClassifier/data/submarino_smartphones.csv', header=True, index=False)
