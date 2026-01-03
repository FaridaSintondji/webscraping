import scrapy
import re
from ..items import ComparateurItem


class ProduitsEyrollesSpider(scrapy.Spider):
    name = "produits_eyrolles"
    allowed_domains = ["www.eyrolles.com", "eyrolles.com"]

    start_urls = [
        "https://www.eyrolles.com/Litterature/Theme/2392/policier-thriller-polars/"
    ]

    def parse(self, response):
        """
        Page catégorie -> récupère tous les liens produit, puis suit chaque lien.
        (logique captures : récupérer tous les href + filtrer /Livre/)
        """

        # 1) récupérer tous les href et filtrer ceux des pages produit
        hrefs = response.xpath("//a/@href").getall()
        book_links = sorted(set([h for h in hrefs if h and "/Livre/" in h]))

        self.logger.info(f"[EYROLLES] {response.url} -> {len(book_links)} liens livres")
        if book_links:
            self.logger.info(f"[EYROLLES] exemple lien : {book_links[0]}")

        for lien in book_links:
            item = ComparateurItem()

            #Récupération du lien du livre
            item["url"] = response.urljoin(lien)

            yield response.follow(
                lien,
                callback=self.parse_lien,
                #utilisation de cb_kwargs pour passer l'objet item à la classe parse_lien
                cb_kwargs={"item": item},
            )

        # 2) pagination (si présente) - logique captures (plusieurs fallbacks)
        next_page = (
            response.css("a.action.next::attr(href)").get()
            or response.xpath("//a[contains(., 'Suivant')]/@href").get()
            or response.xpath("//a[contains(@class,'next')]/@href").get()
            or response.xpath("//a[@rel='next']/@href").get()
        )

        if next_page:
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
