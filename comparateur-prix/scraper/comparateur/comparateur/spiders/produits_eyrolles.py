import scrapy
import re
from ..items import ComparateurItem


class ProduitsEyrollesSpider(scrapy.Spider):
    name = "produits_eyrolles"
    allowed_domains = ["www.eyrolles.com", "eyrolles.com"]

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
        Page produit -> extrait titre, prix, ean, url
        """

        item["site"] = "Eyrolles"
        item["url"] = response.url

        #Récupération du titre du livre
        titre = response.css("h1::text").get()
        if not titre:
            titre = response.xpath("//h1/text()").get()
        item["titre"] = titre.strip() if titre else None

        #Récupération du prix (brut) -> nettoyage géré par le pipeline
        # (logique capture : récupérer le content/@content si dispo)
        prix = response.xpath("string(//p[contains(@class,'prix')]/@content)").get()
        if not prix:
            # fallback: texte affiché
            morceaux = response.xpath("//p[contains(@class,'prix')]//text()").getall()
            morceaux = [m.strip() for m in morceaux if m.strip()]
            prix = "".join(morceaux) if morceaux else None
        item["prix"] = prix

        # Si pas de titre ou pas de prix → on ignore cette page
        if not titre or not prix:
            return

        item['titre']=titre
        item['prix']=prix
        item['site']='Eyrolles'
        #Récupération de l'EAN
        ean = response.xpath("string(//td[contains(@itemprop,'gtin13')]/@content)").get()
        if not ean:
            # fallback au texte si jamais
            ean = response.xpath(
                "string(//td[contains(.,'EAN')]/following-sibling::td[1])"
            ).get()

        if ean:
            ean = re.sub(r"\D", "", ean)
            if len(ean) != 13:
                ean = None
        item["ean"] = ean

        yield item
