import csv
import json
import re


def list_from_csv(csv_name):
  product_values_per_row = 58
  first_product_value = 2
  values_per_product = 3
  with open(csv_name, newline='') as csvfile:
    file = csv.reader(csvfile, delimiter=',')
    next(file, None)
    ingredients = []
    quantities = []
    units = []
    titles = []
    directions = []
    for row in file:
      for i in range(first_product_value, product_values_per_row, values_per_product):
        quantities.append(row[i])
        units.append(row[i+1])
        ingredients.append(row[i+2])
      titles.append(row[0])
      directions.append(row[1])
    data = [titles, directions, quantities, units, ingredients]
  return data


def clean_quantity_names(quantities):
  tuples_to_replace = [("2-Jan", "1/2"), ("3-Jan", "1/3"), ("4-Jan", "1/4"), 
                        ("8-Jan", "1/8"), ("3-Feb", "2/3"), ("4-Mar", "3/4")]
  for pair in tuples_to_replace:
    quantities = list(map(lambda item: item.replace(pair[0], pair[1]), quantities))
  return quantities


def clean_product_names(products):
  uneeded_words = ["grated", "sliced", "crushed", "spoonful of", "unsifted", 
                  "sifted", "shredded","to taste", "finely", "chopped", "stewed", 
                  "diced", "melted", "very", "fine ", "hot cooked", "cold", "large", 
                  "mashed", "boiling", "minced", "1/2", "freshly", "fresh", "package of", 
                  "chopped", "pieces", "baked", "beaten", "slices", "for each", ".", "half", 
                  "any ", "ripe", "peeled", "slivered", "crumbled", "small "]
  new_list = map(lambda product: product.split(",", 1)[0], products)
  new_list = map(lambda product: product.replace("10", "ten"), new_list)
  new_list = map(lambda product: product.replace("1", "one"), new_list)
  new_list = map(lambda product: product.split(" (", 1)[0], new_list)
  new_list = map(lambda product: product.split(" or ")[0], new_list)
  new_list = map(lambda product: product.split(" and ")[0], new_list)
  new_list = map(lambda product: product.lower(), new_list)
  for word in uneeded_words:
    new_list = map(lambda product: product.replace(word, ""), new_list)
  new_list = map(lambda product: re.sub("\s\s+", " ", product), new_list)
  new_list = list(map(lambda product: product.strip(), new_list))
  for i in range(len(new_list)):
    plural1 = f"{new_list[i]}s"
    plural2 = f"{new_list[i]}es"
    if plural1 in new_list:
      new_list[i] = plural1
    if plural2 in new_list:
      new_list[i] = plural2
  return list(new_list)


def create_products_inital_data(ingredients, quantities, units):
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
  return (product_data, product_in_recipe_data)


def create_recipes_initial_data(titles, directions):
  recipes_data = [
    {"model": "recipes.recipe", "pk": i, "fields": {
      "title": titles[i],
      "directions": directions[i]
      }
    } for i in range(len(titles))]
  return recipes_data


def create_json_file(data):
  titles = data[0]
  directions = data[1]
  quantities = data[2]
  units = data[3]
  ingredients = data[4]

  quantities = clean_quantity_names(quantities)
  ingredients = clean_product_names(ingredients)

  products_tuple = create_products_inital_data(ingredients, quantities, units)
  recipes_data = create_recipes_initial_data(titles, directions)
  
  json_data = recipes_data + products_tuple[0] + products_tuple[1]
  return json_data

csv_name = "../../recipes.csv"
data = list_from_csv(csv_name)
json_data = create_json_file(data)

with open("initial_data.json",'w') as f: 
  json.dump(json_data, f, indent=1) 