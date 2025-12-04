import scrapy


class ProduitsMomoxSpider(scrapy.Spider):
    name = "produits_momox"
    allowed_domains = ["comparateur"]
    start_urls = ["https://comparateur"]

    def parse(self, response):
        pass
