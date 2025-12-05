import scrapy
#Import de la classe ComparateurItem créée dans le fichier items
from ..items import ComparateurItem

class ProduitsDecitreSpider(scrapy.Spider):
    name = "produits_decitre"
    allowed_domains = ["www.decitre.fr"]
    start_urls = ["https://www.decitre.fr/livres.html"]

    def parse(self, response):
        
        books = response.xpath('//div[@class="product-card-infos"]')
        
        for book in books:
            item = ComparateurItem()
            #Récupération du lien du livre
            lien =book.xpath('./div[@class="product-card-infos__details"]/div[@class="product-card-infos__details__texts"]/a/@href').get()
            #Utilisation de urljoin pour transformer le lien récupéré en un vrai lien qui marche
            item['url'] = response.urljoin(lien)
            #On vérifie si le lien existe
            if lien:
                yield response.follow(lien, 
                                    callback = self.parse_lien,
                                    #utilisation de cb_kwargs pour passer l'objet item à la classe parse_lien
                                    cb_kwargs={'item':item})
            
            

    def parse_lien(self, response, item):
        #Récupération du titre du livre
        item['titre'] = response.xpath('//h1/text()').get()
        #Récupération du prix
        item['prix'] = response.xpath('//a[@class="product-button selected link--active"]/div[@class="price"]/text()').get()
        yield item
            
            