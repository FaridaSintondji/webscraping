import scrapy
from ..items import ComparateurItem


class ProduitsMollatSpider(scrapy.Spider):
    name = "produits_mollat"
    allowed_domains = ["www.mollat.com"]
    start_urls = [
        "https://www.mollat.com/Recherche?requete=McFadden%2C%20Freida"
    ]

    def parse(self, response):
        """
        PAGE DE RESULTATS MOLLAT
        - récupérer les blocs de livres
        - trouver les liens vers les pages détails
        - suivre chaque lien vers parse_lien()
        """

        livres = response.xpath('//div[@class="notice-embed"]')

        self.logger.info(f"NB BLOCS TROUVÉS : {len(livres)}")

        for livre in livres:
            item = ComparateurItem()

            lien = livre.xpath('.//a/@href').get()
            item["url"] = response.urljoin(lien)
            if lien:
                yield response.follow(lien, callback=self.parse_lien)

        # pagination Mollat 
        next_page = response.css("a[href*='page=']::attr(href)").getall()
        for href in next_page:
            yield response.follow(href, callback=self.parse)

    def parse_lien(self, response):
        item = ComparateurItem()

    def parse_lien(self, response, item):
        """
        PAGE DETAIL MOLLAT
        - récupérer titre & prix
        """

        titre = response.xpath('//h1/text()').get()
        prix = response.xpath('//div[@class="main-panel center"]/div[@class="notice-price notice-price-big"]/text()').get()

        if not titre or not prix:
            self.logger.warning(f"Page ignorée : titre/prix manquant → {response.url}")
            return

        item["titre"] = titre
        item["prix"] = prix
        item["site"] = "Mollat"
        item["url"] = response.url

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
