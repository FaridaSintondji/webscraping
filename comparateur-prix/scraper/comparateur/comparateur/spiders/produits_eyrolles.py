import scrapy
from ..items import ComparateurItem

class ProduitsEyrollesSpider(scrapy.Spider):
    name = "produits_eyrolles"
    allowed_domains = ["www.eyrolles.com"]
    start_urls = [
        "https://www.eyrolles.com/Recherche/?q=Auteur%20:%20Freida%20McFadden"
    ]

    def parse(self, response):
        """
        PAGE DE RESULTATS
        - on récupère les liens des livres
        - on suit chaque lien vers parse_lien
        """

        livres = response.xpath("//a[contains(@href, '/Livre/')]")

        self.logger.info(f"NB LIENS TROUVES: {len(livres)}")

        for livre in livres:
            item = ComparateurItem()
            lien = livre.xpath("./@href").get()
            item['url'] = response.urljoin(lien)
            if lien:
                yield response.follow(lien, callback=self.parse_lien, cb_kwargs={'item':item})

        # Pagination (si jamais il y a une page suivante)
        next_page = response.xpath('//a[@aria-label="Suivant"]/@href').get()

        if next_page:
            self.logger.info(f"Eyrolles - Page suivante trouvée : {next_page}")
            
            yield response.follow(next_page, callback=self.parse)

    
    def parse_lien(self, response, item):
        """
        PAGE DETAIL D'UN LIVRE
        - on récupère le titre et le prix
        """

        titre = response.xpath("//h1[@class='grisbleudense']/text()").get()
        prix = response.xpath("//p[@class='prix']/@content").get()

        if prix is None:
            morceaux = response.xpath("//p[@class='prix']//text()").getall()
            morceaux = [m.strip() for m in morceaux if m.strip()]
            prix = "".join(morceaux)

        # Si pas de titre ou pas de prix → on ignore cette page
        if not titre or not prix:
            return

        item['titre']=titre
        item['prix']=prix
        item['site']='Eyrolles'

        yield item

