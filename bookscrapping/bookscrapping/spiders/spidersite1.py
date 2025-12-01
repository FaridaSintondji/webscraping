import scrapy


class Spidersite1Spider(scrapy.Spider):
    name = "spidersite1"
    allowed_domains = ["bookscrapping"]
    start_urls = ["https://bookscrapping"]

    def parse(self, response):
        pass
