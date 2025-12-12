import scrapy
from ..items import ComparateurItem

class ProduitsMollatSpider(scrapy.Spider):
    name = "produits_mollat"
    allowed_domains = ["www.mollat.com"]
    
    # Page de recherche
    start_urls = [
        "https://www.mollat.com"
    ]

    def parse(self, response):
        """
        PAGE DE RESULTATS MOLLAT
        - récupérer les blocs de livres
        - trouver les liens vers les pages détails
        - suivre chaque lien vers parse_lien()
        """

        livres = response.xpath('//div[@class="center"]')

        self.logger.info(f"NB BLOCS TROUVÉS : {len(livres)}")

        for livre in livres:
            item = ComparateurItem()

            lien = livre.xpath('./div[@class="notice-title h3"]/a/@href').get()
            item["url"] = response.urljoin(lien)
            if lien:
                

                yield response.follow(
                    lien,
                    callback=self.parse_lien,
                    cb_kwargs={'item': item}
                )

        

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

        yield item
