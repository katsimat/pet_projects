import pandas as pd
import csv
import numpy as np
from random import randint
import random
from datetime import time, timedelta, datetime

n = 1000  # Количество пар (можно изменить)
max_dishes = 50  # Максимальное значение id_dishes
max_products = 100  # Максимальное значение id_products

# Генерируем все возможные комбинации и выбираем n уникальных пар
dishes = np.random.randint(1, max_dishes + 1, size=n)
products = np.random.randint(1, max_products + 1, size=n)
pairs = np.column_stack((dishes, products))

# Проверяем уникальность пар и заменяем дубликаты, если есть
unique_pairs, indices = np.unique(pairs, axis=0, return_index=True)
while len(unique_pairs) < n:
    additional_n = n - len(unique_pairs)
    new_dishes = np.random.randint(1, max_dishes + 1, size=additional_n)
    new_products = np.random.randint(1, max_products + 1, size=additional_n)
    new_pairs = np.column_stack((new_dishes, new_products))
    pairs = np.vstack((unique_pairs, new_pairs))
    unique_pairs = np.unique(pairs, axis=0)
    if len(unique_pairs) > n:
        unique_pairs = unique_pairs[:n]

# Разделяем на два массива
id_dishes = unique_pairs[:, 0]
id_products = unique_pairs[:, 1]

weight_product = np.array(np.random.uniform(low=0.1, high=100, size=n))

# id,id_dishes,id_products,weight_product
with open('dishes_products.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    header = ['id', 'id_dishes', 'id_products', 'weight_product']
    writer.writerow(header)
    for i in range(n):
        writer.writerow([i + 1,
                         id_dishes[i],
                         id_products[i],
                         weight_product[i]
                        ])
