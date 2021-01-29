import csv
import json
import re


def list_from_csv(csv_name):
  with open(csv_name, newline='') as csvfile:
    file = csv.reader(csvfile, delimiter=',')
    next(file, None)
    ingredients = []
    quantities = []
    units = []
    titles = []
    directions = []
    for row in file:
      for i in range(2,58,3):
        quantities.append(row[i])
        units.append(row[i+1])
        ingredients.append(row[i+2])
      titles.append(row[0])
      directions.append(row[1])
    data = [titles, directions, quantities, units, ingredients]
  return data


def clean_quantity_names(quantities):
  quantities = list(map(lambda item: item.replace("2-Jan", "1/2"), quantities))
  quantities = list(map(lambda item: item.replace("3-Jan", "1/3"), quantities))
  quantities = list(map(lambda item: item.replace("4-Jan", "1/4"), quantities))
  quantities = list(map(lambda item: item.replace("8-Jan", "1/8"), quantities))
  quantities = list(map(lambda item: item.replace("3-Feb", "2/3"), quantities))
  quantities = list(map(lambda item: item.replace("4-Mar", "3/4"), quantities))
  return quantities


def clean_product_names(products):
  uneeded_words = ["grated", "sliced", "crushed", "spoonful of", "unsifted", "sifted", "shredded","to taste", "finely", "chopped", "stewed", "diced", "melted", "very", "fine ", "hot cooked", "cold", "large", "mashed", "boiling", "minced", "1/2", "freshly", "fresh", "package of", "chopped", "pieces", "baked", "beaten", "slices", "for each", ".", "half", "any ", "ripe", "peeled", "slivered", "crumbled", "small "]
  
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
  #zamiana liczby pojedynczej na mnogą
  for i in range(len(new_list)):
    plural1 = new_list[i] + "s"
    plural2 = new_list[i] + "es"
    if plural1 in new_list:
      new_list[i] = plural1
    if plural2 in new_list:
      new_list[i] = plural2
  return new_list

csv_name = "../../recipes.csv"
data = list_from_csv(csv_name)

titles = data[0]
directions = data[1]
quantities = data[2]
units = data[3]
ingredients = data[4]

quantities = clean_quantity_names(quantities)
ingredients = clean_product_names(ingredients)

product_data = []
product_in_recipe_data = []

for i in range(len(ingredients)):
  if ingredients[i] != '':
    if ingredients[i] not in ingredients[:i]:
      new_product = {"model": "products.product", "pk": i, "fields": {
        "name": ingredients[i]}
        }
      new_product_in_recipe = {"model": "recipes.productinrecipe", "pk": i, "fields": {
        "product": i,
        "recipe": i//19,
        "quantity": quantities[i],
        "unit": units[i]}
        }
      product_data.append(new_product)
      product_in_recipe_data.append(new_product_in_recipe)
    else:
      index = ingredients.index(ingredients[i])
      new_product_in_recipe = {"model": "recipes.productinrecipe", "pk": i, "fields": {
        "product": index,
        "recipe": i//19,
        "quantity": quantities[i],
        "unit": units[i]}
        }
      product_in_recipe_data.append(new_product_in_recipe)

recipes_data = [{"model": "recipes.recipe", "pk": i, "fields": {
  "title": titles[i],
  "directions": directions[i]}
  } for i in range(len(titles))]

json_data = recipes_data + product_data + product_in_recipe_data

with open("initial_data.json",'w') as f: 
  json.dump(json_data, f, indent=1) 