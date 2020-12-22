import nltk
import csv
import json
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import pymongo

def filter(fileName='data/bun_presentasi.csv'):
    new_item_file = open('data/data_toko.json', 'w', encoding='utf-8',  newline='\n')
    all_products = {"product_list":
        []
    }
    # INDEXING STARTS FROM 0
    # id -> column 1
    # nama -> column 2
    # URL -> column 3
    # stok -> column 4
    # status -> column 8
    # harga -> column 9
    with open(fileName, 'r', encoding='cp1252', newline='') as item_file:
        item_file = csv.reader(item_file)
        for i in range(3):
            next(item_file)

        for item in item_file:
            cur_status = item[8]
            cur_stock = item[4]
            if(cur_status == 'Nonaktif' or cur_stock == 0):
                continue
            else:
                cur_id = item[1]
                cur_name = item[2]
                cur_url = item[3]
                cur_price = item[9]

                unwantedChar = ['-', '\"', '\'', '\\', '/', '(', ')', 'atau', 'dan']
                # remove useless characters
                cur_name = cur_name.lower()
                for items in unwantedChar:
                    cur_name = cur_name.replace(items, ' ')
                # get every component of the name
                cur_name = cur_name.split(' ')
                temp_cur_name = []
                for tags in cur_name:
                    if tags == '':
                        continue
                    else:
                        temp_cur_name.append(tags)
    
            product = {
                "id": cur_id, 
                "tags": temp_cur_name,
                "url": cur_url,
                "price": cur_price,
                "stock": cur_stock
            }
            all_products['product_list'].append(product)
    
        json.dump(all_products, new_item_file)
        new_item_file.close()
        print("SUCCESS")


def edit_database(insert_new_data=False, path_to_new_data=None, new_table_name=None, table_name_check=False, data_check=False):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["rina_bot_database"]

    # MAU NGECEK TABEL APA AJA YANG ADA DI DATABASE
    if table_name_check == True:
        print("HERE ARE THE LISTS OF RINABOT'S DATABASE TABLES NAME")
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["rina_bot_database"]
        print(mydb.list_collection_names())

    # KALAU MAU INSERT DATA BARU, LIHAT FILE PATHNYA
    if insert_new_data == True and path_to_new_data != None and new_table_name != None:
        table_products = mydb[new_table_name]
        with open(path_to_new_data) as item_file:
            all_products = json.load(item_file)

            for products in all_products["product_list"]:
                table_products.insert_one(products)
        print("NEW DATA INSERTED!")
    
    # LIHAT BARANG APA SAJA YANG SUDAH ADA DI TABEL
    if data_check == True and new_table_name != None:
        table_products = mydb[new_table_name]
        print(table_products.count_documents({}))

if __name__ == '__main__':
    filter()
    edit_database(insert_new_data=False, path_to_new_data="data/data_toko.json", new_table_name="bunshopz", table_name_check=True, data_check=True)