import scrapy


class Spidersite3Spider(scrapy.Spider):
    name = "spidersite3"
    allowed_domains = ["bookscrapping"]
    start_urls = ["https://bookscrapping"]

    def parse(self, response):
        pass
