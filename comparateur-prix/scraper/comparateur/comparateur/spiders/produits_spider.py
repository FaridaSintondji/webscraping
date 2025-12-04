import scrapy


class ProduitsSpiderSpider(scrapy.Spider):
    name = "produits_spider"
    allowed_domains = ["comparateur"]
    start_urls = ["https://comparateur"]

    def parse(self, response):
        pass
