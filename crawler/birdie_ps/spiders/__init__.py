import scrapy
import pandas as pd

class SmartphoneSpider(scrapy.Spider):
    name = 'smartphone_spider'
    start_urls = ['https://www.submarino.com.br/categoria/celulares-e-smartphones/smartphone']
    data = pd.DataFrame(columns=['url', 'smartphone'])
    total_scrapped = 0

    def parse(self, response):
        SET_SELECTOR = '.hUksZj'
        for smartphone in response.css(SET_SELECTOR):
            NAME_SELECTOR = '.YHJwU ::text'
            new_smartphone = smartphone.css(NAME_SELECTOR).extract_first()
            yield {'name': new_smartphone}

            # Adiciona ao df
            self.data.loc[self.total_scrapped, 'url'] = response.request.url
            self.data.loc[self.total_scrapped, 'smartphone'] = new_smartphone
            self.total_scrapped += 1

        # Busca proxima pagina
        NEXT_PAGE_SELECTOR = '#content-middle li:nth-child(10) a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        print(self.total_scrapped)
        self.data.to_csv('/Users/joao/Desktop/SmartphoneClassifier/data/submarino_smartphones.tsv', header=True, index=False, sep='\t')
