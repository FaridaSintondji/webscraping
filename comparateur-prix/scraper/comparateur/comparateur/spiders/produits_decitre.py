import scrapy
from ..items import ComparateurItem

class ProduitsDecitreSpider(scrapy.Spider):
    name = "produits_decitre"
    allowed_domains = ["www.decitre.fr/"]
    start_urls = ["https://www.decitre.fr/"]

    def parse(self, response):
        
        books = response.xpath('//div[@class="product-card-infos"]')
        
        for book in books:
            item = ComparateurItem()
            item['titre'] = book.xpath('./div[@class="product-card-infos__details"]/div[@class="product-card-infos__details__texts"]/a[@class="product-card-infos__details__texts__link link--active"]/h3[@class="product-card-infos__details__texts__link__title"]/text()').get()
            item['prix'] = book.xpath('./div[@class="product-card-price"]/div[@class="price"]/text()').get()
            item['lien'] = book.xpath('./div[@class="product-card-infos__details"]/div[@class="product-card-infos__details__texts"]/a/@href').get()
            yield item
