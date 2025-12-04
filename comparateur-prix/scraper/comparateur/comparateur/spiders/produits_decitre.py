import scrapy


class ProduitsDecitreSpider(scrapy.Spider):
    name = "produits_decitre"
    allowed_domains = ["comparateur"]
    start_urls = ["https://comparateur"]

    def parse(self, response):
        pass
