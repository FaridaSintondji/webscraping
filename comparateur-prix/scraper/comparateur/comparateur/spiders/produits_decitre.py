import scrapy


class ProduitsDecitreSpider(scrapy.Spider):
    name = "produits_decitre"
    allowed_domains = ["www.decitre.fr/"]
    start_urls = ["https://www.decitre.fr/"]

    def parse(self, response):
        books = response.xpath('//div[@class="product-card-infos"]')
        for book in books:
            titre = book.xpath('./a/h3[@class="product-card-infos__details__texts__link__title"]').get()
            prix = book.xpath('./div[@class="price"]/text()').get()

            yield{
                'titre': titre,
                'prix': prix
            }
