# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ComparateurPipeline:
    def process_item(self, item, spider):
        return item

class NettoyagePipeline:
    def process_item(self, item, spider):
        prix_brut = item['prix']
        #On retire les caractères spéciaux
        prix=prix_brut.replace('\xa0','')
        #On retire le signe de l'euro
        prix=prix.replace('€','')
        #On remplace la virgule par un point pour que le float marche
        prix=prix.replace(',','.')
        #On retire les espaces inutiles
        prix=prix.strip()
        #On convertit le prix en float et on l'arronfit à deux chiffres après la virgule
        prix=round(float(prix), 2)

        item['prix'] = prix
        
        return item