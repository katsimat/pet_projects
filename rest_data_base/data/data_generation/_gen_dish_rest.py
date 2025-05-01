import pandas as pd
import csv
import numpy as np
from random import randint
import random

# Parameters
n = 1000  # Number of pairs
max_dishes = 100  # Maximum id_dishes
max_restaurant = 100  # Maximum id_restaurant

# Load data
dishes = pd.read_csv('dishes.csv')  # Expected columns: id_dishes, price
restaurants = pd.read_csv('restaurant.csv')  # Expected columns: id_restaurant, markup

# Generate n pairs of id_dishes and id_restaurant
id_dishes = np.random.randint(1, max_dishes + 1, size=n)
id_restaurant = np.random.randint(1, max_restaurant + 1, size=n)
pairs = np.column_stack((id_dishes, id_restaurant))

# Ensure unique pairs
unique_pairs = np.unique(pairs, axis=0)
while len(unique_pairs) < n:
    additional_n = n - len(unique_pairs)
    new_id_dishes = np.random.randint(1, max_dishes + 1, size=additional_n)
    new_id_restaurant = np.random.randint(1, max_restaurant + 1, size=additional_n)
    new_pairs = np.column_stack((new_id_dishes, new_id_restaurant))
    pairs = np.vstack((unique_pairs, new_pairs))
    unique_pairs = np.unique(pairs, axis=0)
    if len(unique_pairs) > n:
        unique_pairs = unique_pairs[:n]

# Extract id_dishes and id_restaurant
id_dishes = unique_pairs[:, 0]
id_restaurant = unique_pairs[:, 1]

# Calculate price_in_rest = price * markup
dishes_dict = dishes.set_index('id_dishes')['price'].to_dict()
restaurant_dict = restaurants.set_index('id_restaurant')['markup'].to_dict()

price_in_rest = []
for dish_id, rest_id in zip(id_dishes, id_restaurant):
    price = dishes_dict.get(dish_id, 0)  # Default to 0 if id not found
    markup = restaurant_dict.get(rest_id, 1)  # Default to 1 if id not found
    price_in_rest.append(round(price * markup, 2))

# Write to CSV: id, id_dishes, id_restaurant, price_in_rest
with open('dishes_restaurant_new.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    header = ['id', 'id_dishes', 'id_restaurant', 'price_in_rest']
    writer.writerow(header)
    for i in range(n):
        writer.writerow([
            i + 1,
            id_dishes[i],
            id_restaurant[i],
            price_in_rest[i]
        ])
