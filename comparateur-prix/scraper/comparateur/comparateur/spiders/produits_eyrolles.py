import scrapy


class ProduitsEyrollesSpider(scrapy.Spider):
    name = "produits_eyrolles"
    allowed_domains = ["comparateur"]
    start_urls = ["https://comparateur"]

    def parse(self, response):
        pass
