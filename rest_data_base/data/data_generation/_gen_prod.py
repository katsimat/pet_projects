import pandas as pd
import csv
import numpy as np
from random import randint
import random
from datetime import time, timedelta, datetime

def data_prod():
    '''100 продуктов'''
    food_list = [
        "Salo", "Sweet Potato", "Fig", "Ginger", "Pumpkin", "Burdock Root", "Brussels Sprouts", "Broccoli", "Cauliflower", "Water Chestnut",
        "Cantaloupe", "Prunes", "Octopus", "Carrot", "Winter Squash", "Jalapeño", "Rhubarb", "Almonds", "Walnuts", "Salmon",
        "Spinach", "Kale", "Quinoa", "Chia Seeds", "Flaxseeds", "Oats", "Brown Rice", "Lentils", "Chickpeas", "Black Beans",
        "Avocado", "Blueberries", "Strawberries", "Raspberries", "Blackberries", "Bananas", "Apples", "Oranges", "Mangoes", "Pineapple",
        "Tomatoes", "Cucumbers", "Bell Peppers", "Zucchini", "Eggplant", "Asparagus", "Green Beans", "Peas", "Mushrooms", "Onions",
        "Garlic", "Chicken", "Turkey", "Beef", "Pork", "Eggs", "Yogurt", "Cheese", "Milk", "Butter",
        "Olive Oil", "Coconut Oil", "Honey", "Maple Syrup", "Dark Chocolate", "Tofu", "Tempeh", "Sardines", "Tuna", "Cod",
        "Shrimp", "Crab", "Lobster", "Clams", "Oysters", "Pistachios", "Cashews", "Hazelnuts", "Sunflower Seeds", "Pumpkin Seeds",
        "Wheat Bread", "Rye Bread", "Barley", "Millet", "Buckwheat", "Beets", "Radishes", "Parsnips", "Celery", "Leeks",
        "Arugula", "Swiss Chard", "Collard Greens", "Cabbage", "Seaweed", "Kiwi", "Pomegranate", "Grapes", "Peaches", "Cherries"
    ]
    return food_list

fix_n = 100
name = data_prod()
price = np.round(np.random.uniform(low=1.0, high=100.0, size=fix_n), 2)
id_supplier = np.array([np.random.randint(1, 100) for _ in range(fix_n)])
#id_products,name,price,id_supplier

with open('products_new.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    header = ['id_products', 'name', 'price', 'id_supplier']
    writer.writerow(header)
    for i in range(fix_n):
        writer.writerow([i + 1,
                         name[i],
                         price[i],
                         id_supplier[i]
                        ])
