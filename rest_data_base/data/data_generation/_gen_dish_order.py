import pandas as pd
import csv
import numpy as np
from random import randint
import random
from datetime import time, timedelta, datetime

n = 1000  # Количество пар 
max_dishes = 100  # Максимальное значение id_dishes
max_order = 500  # Максимальное значение id_order

# Генерируем все возможные комбинации и выбираем n уникальных пар
dishes = np.random.randint(1, max_dishes + 1, size=n)
order = np.random.randint(1, max_order + 1, size=n)
pairs = np.column_stack((dishes, order))

# Проверяем уникальность пар и заменяем дубликаты, если есть
unique_pairs, indices = np.unique(pairs, axis=0, return_index=True)
while len(unique_pairs) < n:
    additional_n = n - len(unique_pairs)
    new_dishes = np.random.randint(1, max_dishes + 1, size=additional_n)
    new_products = np.random.randint(1, max_order + 1, size=additional_n)
    new_pairs = np.column_stack((new_dishes, new_products))
    pairs = np.vstack((unique_pairs, new_pairs))
    unique_pairs = np.unique(pairs, axis=0)
    if len(unique_pairs) > n:
        unique_pairs = unique_pairs[:n]

# Разделяем на два массива
id_dishes = unique_pairs[:, 0]
id_order = unique_pairs[:, 1]

cnt_items = np.array([np.random.randint(1,10) for _ in range(n)])

# id,id_dishes,id_order,cnt_items
with open('dishes_order_new.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    header = ['id', 'id_dishes', 'id_order', 'cnt_items']
    writer.writerow(header)
    for i in range(n):
        writer.writerow([i + 1,
                         id_dishes[i],
                         id_order[i],
                         cnt_items[i]
                        ])
