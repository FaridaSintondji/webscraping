import scrapy
from ..items import ComparateurItem

class ProduitsMollatSpider(scrapy.Spider):
    name = "produits_mollat"
    allowed_domains = ["www.mollat.com"]
    
    # Page de recherche
    start_urls = [
        "https://www.mollat.com/recherche?requete=data"
    ]

    def parse(self, response):
        """
        PAGE DE RESULTATS MOLLAT
        - récupérer les blocs de livres
        - trouver les liens vers les pages détails
        - suivre chaque lien vers parse_lien()
        """

        # ----------------------------------------------------
        # XPath pour sélectionner les blocs produits
        # Dans ta capture : //div[contains(@class, "formatable-result-item")]
        # ----------------------------------------------------
        #livres = response.xpath('//div[@class = "notice-content center"]')
        livres = response.xpath('//div[@class ="col-xs-6 col-md-4 formatable-result-item"]/div[@class="notice-embed"]/div[@class = "notice-content center"]')

        self.logger.info(f"NB BLOCS TROUVÉS : {len(livres)}")

        for livre in livres:
            item = ComparateurItem()

            # ----------------------------------------------------
            # XPath pour récupérer le lien du livre
            # Exemple : .//div[@class="notice-title h3"]/a/@href
            # ----------------------------------------------------
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

        # ----------------------------------------------------
        #XPath du titre
        # Exemple probable : //h1/text()
        # ----------------------------------------------------
        titre = response.xpath('//h1/text()').get()

        # ----------------------------------------------------
        # XPath du prix
        # Exemple probable : //div[contains(@class, "notice-price")]/text()
        # ----------------------------------------------------
        prix = response.xpath('//div[@class="main-panel center"]/div[@class="notice-price notice-price-big"]/text()').get()

        # Nettoyage du prix (comme vu en cours)
        if prix:
            prix = prix.replace("€", "").replace(",", ".").strip()

        if not titre or not prix:
            self.logger.warning(f"Page ignorée : titre/prix manquant → {response.url}")
            return

        item["titre"] = titre
        item["prix"] = prix
        item["site"] = "Mollat"

        yield item
