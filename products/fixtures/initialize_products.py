import csv
import json

def product_list_from_csv(csv_name):
  with open(csv_name, newline='') as csvfile:
    file = csv.reader(csvfile, delimiter=',')
    products = set()
    for row in file:
      #dodawanie do zestawu produktów z kolumn z "ingredients"
      for i in range(4,20,3):
        products.add(row[i])
  return list(products)

def clean_product_names(products):
  products.remove("")
  #usuwanie wszystkiego po przecinku
  new_list = list(map(lambda product: product.split(",", 1)[0], products))
  #usuwanie wszystkiego w nawiasie
  new_list = list(map(lambda product: product.split(" (", 1)[0], new_list))
  return new_list

products = product_list_from_csv("recipes.csv")
products = clean_product_names(products)

json_data = [{"model": "products.product", "pk": i, "fields": {"name": name}} for (i, name) in enumerate(products)]

with open("initial_products.json",'w') as f: 
  json.dump(json_data, f, indent=1) 





