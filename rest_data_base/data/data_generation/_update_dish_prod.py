import pandas as pd
import csv
import numpy as np
from random import randint
import random
from datetime import time, timedelta, datetime

def update(n, id_product_target):

    id_dishes = np.array(np.random.choice(range(1, 101), size=n, replace=False))
    weight_product = np.array(np.random.uniform(low=0.5, high=100, size=n))


    with open('dishes_products.csv', 'r', encoding='utf-8') as f:
        lastline = f.readlines()[-1]  # Берем последнюю строку
        last_id = int(lastline.split(',')[0]) 

    with open('dishes_products.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for i in range(n):
            writer.writerow([last_id + i + 1,
                            id_dishes[i],
                            id_product_target,
                            weight_product[i]
                            ])
            
update(52, 41)
for _ in range(40):
    update(random.randint(1, 40), random.randint(1, 41))

