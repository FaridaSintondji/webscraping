import scrapy
from ..items import ComparateurItem

class ProduitsMollatSpider(scrapy.Spider):
    name = "produits_momox"
    allowed_domains = ["momox-shop.fr"]

    start_urls = [
        "https://www.momox-shop.fr/produits-C0/?fcIsSearch=1&searchparam=Freida+McFadden"
    ]

    def parse(self, response):

        livres = response.xpath('//div[@data-testid="product-container"]')
        self.logger.info(f"NB BLOCS TROUVÉS : {len(livres)}")

        for livre in livres:
            lien = livre.xpath('.//a[@href]/@href').get()

            if lien:
                yield response.follow(
                    lien,
                    callback=self.parse_lien
                )

        #Pagination
        next_page = response.xpath('//a[contains(text(), "Continuer")]/@href').get()

        # Si "Continuer" ne marche pas, on essaie de trouver un lien avec "pgNr=" 
        if not next_page:
             # On prend le dernier lien de la liste qui contient pgNr (souvent le suivant)
             all_pages = response.xpath('//a[contains(@href, "pgNr=")]/@href').getall()
             if all_pages:
                 next_page = all_pages[-1]

        if next_page:
            self.logger.info(f"Page suivante trouvée : {next_page}")
            yield response.follow(next_page, callback=self.parse)

    def parse_lien(self, response):

        item = ComparateurItem()

        titre = response.xpath('//h1/text()').get()
        prix = response.xpath('//div[@data-testid="price-display"]/span/text()').get()

        if not titre or not prix:
            self.logger.warning(f"Page ignorée : titre/prix manquant → {response.url}")
            return

        item["titre"] = titre.strip()
        item["prix"] = prix
        item["url"] = response.url
        item["site"] = "Momox"
        #Récupération de l'EAN
        ean = response.xpath('//dd[@class="ProductAttributes_rowValue__fWL3F"]/text()').get()
        item['ean'] = ean

        yield item