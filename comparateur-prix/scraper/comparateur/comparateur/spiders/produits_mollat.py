import scrapy
from ..items import ComparateurItem


class ProduitsMollatSpider(scrapy.Spider):
    name = "produits_mollat"
    allowed_domains = ["www.mollat.com"]
    start_urls = [
        "https://www.mollat.com/litterature/romans-policiers"
    ]

    def parse(self, response):
        livres = response.css("article.notice-embed")

        for livre in livres:
            lien = livre.css(".notice-title a::attr(href)").get()
            if lien:
                yield response.follow(lien, callback=self.parse_lien)

        # pagination Mollat 
        next_page = response.css("a[href*='page=']::attr(href)").getall()
        for href in next_page:
            yield response.follow(href, callback=self.parse)

    def parse_lien(self, response):
        item = ComparateurItem()

        item["site"] = "Mollat"
        item["url"] = response.url

        # Titre
        item["titre"] = response.css("h1::text").get()
        if item["titre"]:
            item["titre"] = item["titre"].strip()

        prix = response.css("div.notice-price.notice-price-big::text").get()
        if not prix:
            prix = response.css("div.notice-price::text").get()
        item["prix"] = prix

        # EAN13
        ean = response.xpath(
            "//strong[normalize-space()='EAN13 :']/following-sibling::span[@class='badge-info']/text()"
        ).get()

        if not ean:
            ean = response.xpath(
                "normalize-space(//strong[contains(normalize-space(.), 'EAN13')]/following::span[@class='badge-info'][1])"
            ).get()

        item["ean"] = ean.strip() if ean else None

        yield item
