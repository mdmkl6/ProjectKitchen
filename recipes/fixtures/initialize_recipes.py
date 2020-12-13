import csv
import json

def list_from_csv(csv_name):
  with open(csv_name, newline='') as csvfile:
    file = csv.reader(csvfile, delimiter=',')
    #pominiecie nagłówków
    next(file, None)
    ingredients = []
    quantities = []
    units = []
    titles = []
    directions = []
    for row in file:
      #dodawanie do zestawu produktów z odpowiednich kolumn
      for i in range(2,58,3):
        quantities.append(row[i])
        units.append(row[i+1])
        ingredients.append(row[i+2])
      titles.append(row[0])
      directions.append(row[1])
    data = [titles, directions, quantities, units, ingredients]
  return data

def clean_quantity_names(quantities):
  #zamiana Jan, Mar itd
  quantities = list(map(lambda item: item.replace("2-Jan", "1/2"), quantities))
  quantities = list(map(lambda item: item.replace("3-Jan", "1/3"), quantities))
  quantities = list(map(lambda item: item.replace("4-Jan", "1/4"), quantities))
  quantities = list(map(lambda item: item.replace("8-Jan", "1/8"), quantities))
  quantities = list(map(lambda item: item.replace("3-Feb", "2/3"), quantities))
  quantities = list(map(lambda item: item.replace("4-Mar", "3/4"), quantities))
  return quantities

csv_name = "../../recipes.csv"
data = list_from_csv(csv_name)

titles = data[0]
directions = data[1]
quantities = data[2]
units = data[3]
ingredients = data[4]

quantities = clean_quantity_names(quantities)

#podział ingredients, units, quantities na podtablice
make_sublists = lambda initial_list, n=19: [initial_list[i:i+n] for i in range(0, len(initial_list), n)]
quantities = make_sublists(quantities)
units = make_sublists(units)
ingredients = make_sublists(ingredients)

#zamiana podtablica na stringi
separator = ", "
units = list(map(lambda sublist: separator.join(sublist), units))
quantities = list(map(lambda sublist: separator.join(sublist), quantities))
ingredients = list(map(lambda sublist: separator.join(sublist), ingredients))

json_data = [{"model": "recipes.recipe", "pk": i, "fields": {
  "title": titles[i],
  "directions": directions[i],
  "units": units[i],
  "quantities": quantities[i],
  "ingredients": ingredients[i]
  }
} for i in range(len(titles))]

with open("initial_recipes.json",'w') as f: 
  json.dump(json_data, f, indent=1) 
