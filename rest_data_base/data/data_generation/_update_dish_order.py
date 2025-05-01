import pandas as pd
import csv
import numpy as np
from random import randint
import random
from datetime import time, timedelta, datetime

def data_id_russian_food(n):
    df = pd.read_csv('dishes_new.csv', encoding='utf-8')
    # Фильтрация блюд русской кухни
    russian_dishes = df[df['cuisine'].str.lower() == 'russian']['id_dishes'].to_numpy()
    return np.array(np.random.choice(russian_dishes, size=n, replace=True))

n = 60
id_order = np.array(np.random.choice(range(100, 500), size=n, replace=False))
id_dishes_target = data_id_russian_food(n)
cnt_items = np.array([np.random.randint(1,10) for _ in range(n)])


with open('dishes_order_new.csv', 'r', encoding='utf-8') as f:
    lastline = f.readlines()[-1]  # Берем последнюю строку
    last_id = int(lastline.split(',')[0]) 

        
with open('dishes_order_new.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    for i in range(n):
        writer.writerow([last_id + i + 1,
                         id_dishes_target[i],
                         id_order[i],
                         cnt_items[i]
                        ])