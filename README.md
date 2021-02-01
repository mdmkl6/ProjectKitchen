# ProjectKitchen
## General info
This application helps people in managing their kitchen. 
It stores the data of all products that user has in the kitchen. On that basis it offers various recipes that user may try and rate. 
Recipes are also suggested by the recommender system based on other users' ratings. Additional feature to this app is a shopping list.

## Technologies
This application is created with Django 3.0.2

## Setup
To use the application run following commands:
* pip install -r requirements.txt
* python manage.py migrate
* python manage.py loaddata initial_data
* python manage.py runserver
