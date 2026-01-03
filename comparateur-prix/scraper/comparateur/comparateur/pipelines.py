# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector

class ComparateurPipeline:
    def process_item(self, item, spider):
        return item

class NettoyagePipeline:
    def process_item(self, item, spider):

        prix = item.get("prix")

        # Si déjà float → on ne touche pas
        if isinstance(prix, (float, int)):
            item["prix"] = round(float(prix), 2)
            return item

        if isinstance(prix, str):
            try:
                prix = (
                    prix.replace("\xa0", "")
                        .replace("€", "")
                        .replace(",", ".")
                        .strip()
                )
                item["prix"] = round(float(prix), 2)
            except:
                item["prix"]=None

        return item

    
class MysqlPipeline:
    def process_item(self, item, spider):
        mydb = mysql.connector.connect(
            host="db",
            user="toto",
            password="toto",
            database="Produits"
        )
        mycursor=mydb.cursor()

    

        sql = "INSERT INTO Livre (titre, prix, url, site, ean) VALUES (%s, %s, %s, %s, %s)"
        val = (
            item.get('titre'),
            item.get('prix'),
            item.get('url'),
            item.get('site'),
            item.get('ean')
        )
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")

        return item
