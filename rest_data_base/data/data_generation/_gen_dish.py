import pandas as pd
import csv
import numpy as np
from random import randint
import random
from datetime import time, timedelta, datetime

def generate_dishes_and_cuisines():
    # Кухни и их возможные блюда (примеры)
    cuisines_data = {
        "American": [
            "New York Cheesecake", "Chicago Hot Dog", "BBQ Pork Ribs", "Buffalo Wings", "Mac and Cheese",
            "Apple Pie", "Clam Chowder", "Pancakes", "Cornbread", "Cobb Salad",
            "Reuben Sandwich", "Philly Cheesesteak", "Gumbo", "Jambalaya", "Key Lime Pie",
            "Peanut Butter Cookies", "Fried Green Tomatoes", "Lobster Roll", "Cajun Shrimp", "S'mores"
        ],
        "Korean": [
            "Bibimbap", "Kimchi Jjigae", "Bulgogi", "Tteokbokki", "Samgyeopsal",
            "Japchae", "Haemul Pajeon", "Sundubu Jjigae", "Galbi", "Dakgangjeong",
            "Gimbap", "Kimchi Fried Rice", "Budae Jjigae", "Hobakjuk", "Naengmyeon",
            "Yukgaejang", "Bingsu", "Eomuk Tang", "Jjajangmyeon", "Patbingsu"
        ],
        "Russian": [
            "Borscht", "Beef Stroganoff", "Olivier Salad", "Pelmeni", "Blini with Caviar",
            "Solyanka", "Syrniki", "Pirozhki", "Shchi", "Kholodets",
            "Kvas", "Medovik", "Vareniki", "Golubtsy", "Okroshka",
            "Seledka Pod Shuboy", "Rassolnik", "Kulebyaka", "Draniki", "Zakuski Platter"
        ],
        "Japanese": [
            "Sushi", "Ramen", "Tempura", "Takoyaki", "Miso Soup",
            "Tonkatsu", "Yakitori", "Sashimi", "Okonomiyaki", "Udon",
            "Donburi", "Chawanmushi", "Kaiseki", "Oden", "Unagi Don",
            "Matcha Ice Cream", "Gyudon", "Agedashi Tofu", "Onigiri", "Mochi"
        ],
        "Indian": [
            "Butter Chicken", "Palak Paneer", "Biryani", "Samosa", "Chana Masala",
            "Dosa", "Vindaloo", "Pani Puri", "Rogan Josh", "Malai Kofta",
            "Tandoori Chicken", "Aloo Gobi", "Naan", "Dal Tadka", "Gulab Jamun",
            "Pav Bhaji", "Korma", "Idli", "Raita", "Jalebi"
        ],
        "Mexican": [
            "Tacos al Pastor", "Enchiladas", "Mole Poblano", "Pozole", "Chiles en Nogada",
            "Ceviche", "Tamales", "Chilaquiles", "Quesadillas", "Guacamole",
            "Elote", "Tostadas", "Sopes", "Menudo", "Carnitas",
            "Horchata", "Flan", "Churros", "Birria", "Agua Fresca"
        ]
    }

    # Распределение количества блюд по кухням (сумма = 100)
    total_dishes = 100
    num_cuisines = len(cuisines_data)
    base_per_cuisine = total_dishes // num_cuisines  # ~16-17 на кухню
    remaining = total_dishes % num_cuisines

    # Генерация случайных количеств (от 5 до 20) с балансировкой
    dish_counts = {}
    for cuisine in cuisines_data:
        dish_counts[cuisine] = random.randint(5, 20)

    # Корректировка суммы до 100
    while sum(dish_counts.values()) != total_dishes:
        diff = total_dishes - sum(dish_counts.values())
        for cuisine in dish_counts:
            if diff > 0 and dish_counts[cuisine] < 20:
                dish_counts[cuisine] += 1
                diff -= 1
            elif diff < 0 and dish_counts[cuisine] > 5:
                dish_counts[cuisine] -= 1
                diff += 1
            if diff == 0:
                break

    # Формирование итоговых списков
    dishes = []
    cuisines = []
    for cuisine, count in dish_counts.items():
        selected_dishes = random.sample(cuisines_data[cuisine], count)
        dishes.extend(selected_dishes)
        cuisines.extend([cuisine] * count)

    return dishes, cuisines


def update_price(n):
    dishes_products = pd.read_csv('dishes_products.csv')
    products = pd.read_csv('products.csv')
    
    merged = pd.merge(dishes_products, products, on='id_products', how='left')
    merged['ingredient_cost'] = merged['price'] * merged['weight_product']
    
    dishescost = merged.groupby('id_dishes')['ingredient_cost'].sum().reset_index()
    dishescost.columns = ['id_dishes', 'total_price']
    
    return dishescost['total_price'].head(n).tolist()



# Пример использования
name, cuisine = generate_dishes_and_cuisines()
n = 100

price = update_price(n)
#id_dishes,name,cuisine,price

with open('dishes_new.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    header = ['id_dishes', 'name', 'cuisine', 'price']
    writer.writerow(header)
    for i in range(n):
        writer.writerow([i + 1,
                         name[i],
                         cuisine[i],
                         round(price[i], 2)
                        ])






