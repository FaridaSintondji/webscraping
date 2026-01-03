import scrapy
#Import de la classe ComparateurItem créée dans le fichier items
from ..items import ComparateurItem


class ProduitsDecitreSpider(scrapy.Spider):
    name = "produits_decitre"
    allowed_domains = ["www.decitre.fr"]

    # Tu peux garder livres.html si tu veux (comme ton fichier)
    # start_urls = ["https://www.decitre.fr/livres.html"]

    # URL plus "thématique" (si tu veux tester sur Polars nouveautés)
    start_urls = ["https://www.decitre.fr/livres/litterature/polars/nouveautes.html"]

    def parse(self, response):

        books = response.xpath('//div[@class="product-card-infos"]')

        for book in books:
            item = ComparateurItem()
            #Récupération du lien du livre
            lien = book.xpath('./div[@class="product-card-infos__details"]/div[@class="product-card-infos__details__texts"]/a/@href').get()

            #On vérifie si le lien existe
            if lien:
                #Utilisation de urljoin pour transformer le lien récupéré en un vrai lien qui marche
                item['url'] = response.urljoin(lien)

                yield response.follow(
                    lien,
                    callback=self.parse_lien,
                    #utilisation de cb_kwargs pour passer l'objet item à la classe parse_lien
                    cb_kwargs={'item': item}
                )

        # --- Pagination : page suivante
        next_page = response.css("a[rel='next']::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_lien(self, response, item):
        #Récupération du titre du livre
        item['titre'] = response.xpath('//h1/text()').get()
        prix = response.xpath('//a[@class="product-button selected link--active"]/div[@class="price"]/text()').get()
        # Fallback plus robuste au cas où la classe exacte change
        if not prix:
            prix = response.xpath('//a[contains(@class,"product-button")]//div[contains(@class,"price")]/text()').get()
        item['prix'] = prix
        #Récupération de l'EAN
        ean = response.xpath("//span[normalize-space(text())='EAN']/following-sibling::span[1]/text()").get()
        item['ean'] = ean
        item['site'] = 'Decitre'
        yield item
