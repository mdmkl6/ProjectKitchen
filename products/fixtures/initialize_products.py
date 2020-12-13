import csv
import json
import re

def product_list_from_csv(csv_name):
  with open(csv_name, newline='') as csvfile:
    file = csv.reader(csvfile, delimiter=',')
    products = set()
    for row in file:
      #dodawanie do zestawu produktów z kolumn z "ingredients"
      for i in range(4,58,3):
        products.add(row[i])
  return list(products)

def clean_product_names(products):
  uneeded_words = ["grated", "sliced", "crushed", "spoonful of", "unsifted", "sifted", "shredded","to taste", "finely", "chopped", "stewed", "diced", "melted", "very", "fine", "cold", "hot cooked", "cold", "large", "mashed", "boiling", "minced", "1/2", "freshly", "fresh", "package of", "chopped", "pieces", "baked", "beaten", "slices", "for each", ".", "half", "any ", "ripe", "peeled", "slivered"]
  #usuwanie elementów ingredientXY od 01 do 06
  for i in range(1,10):
    products.remove("Ingredient0" + str(i))
  for i in range(0,9):
    products.remove("Ingredient1" + str(i))
  #usuwanie wszystkiego po przecinku
  new_list = list(map(lambda product: product.split(",", 1)[0], products))
  #naprawa 10 i 1 na słowne
  new_list = list(map(lambda product: product.replace("10", "ten"), new_list))
  new_list = list(map(lambda product: product.replace("1", "one"), new_list))
  #usuwanie wszystkiego w nawiasie
  new_list = list(map(lambda product: product.split(" (", 1)[0], new_list))
  #produkty z or lub and (pierwsza czesc zostaje)
  new_list = list(map(lambda product: product.split(" or ")[0], new_list))
  new_list = list(map(lambda product: product.split(" and ")[0], new_list))
  #wszystko na małe litery
  new_list = list(map(lambda product: product.lower(), new_list))
  #usuwanie niepotrzebnych słów
  for word in uneeded_words:
    new_list = list(map(lambda product: product.replace(word, ""), new_list))
  #usuwanie zbednych spacji
  new_list = list(map(lambda product: re.sub("\s\s+", " ", product), new_list))
  #usuwanie zbędnych spacji na końcu produktu
  new_list = list(map(lambda product: product.strip(), new_list))
  #usuwanie powtarzajacych sie elementow
  new_list = list(set(new_list))
  #usuwanie liczby pojedynczej jesli wystepuje mnoga
  for word in new_list:
    plural1 = word + "s"
    plural2 = word + "es"
    if plural1 in new_list or plural2 in new_list:
      new_list.remove(word)
  #usuniecie pustych stringów
  new_list.remove("")
  #Sprawdzenie ilości produktów
  print(len(new_list))
  print(new_list)
  return new_list

cvs_name = "../../recipes.csv"
products = product_list_from_csv(cvs_name)
products = clean_product_names(products)

json_data = [{"model": "products.product", "pk": i, "fields": {"name": name}} for (i, name) in enumerate(products)]

with open("initial_products.json",'w') as f: 
  json.dump(json_data, f, indent=1) 

#Teraz żeby zainicjalizować produkty wystarczy wpisać komendę:
#python manage.py loaddata initial_products.json
