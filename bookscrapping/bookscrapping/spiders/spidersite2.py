import scrapy


class Spidersite2Spider(scrapy.Spider):
    name = "spidersite2"
    allowed_domains = ["bookscrapping"]
    start_urls = ["https://bookscrapping"]

    def parse(self, response):
        pass
