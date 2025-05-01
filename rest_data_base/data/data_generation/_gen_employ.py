import pandas as pd
import csv
import numpy as np
from random import randint
import random
from datetime import time, timedelta, datetime

def data_firstname(n):
    firstnames = ['James', 'Emma', 'Liam', 'Olivia', 'Noah', 'Ava', 'Ethan', 'Sophia', 'Mason', 'Isabella']
    return [random.choice(firstnames) for _ in range(n)]
def data_surname(n): 
    surnames = ['Smith', 'Johnson', 'Brown', 'Taylor', 'Wilson', 'Davis', 'Clark', 'Harris', 'Lewis', 'Walker']
    return [random.choice(surnames) for _ in range(n)]
def data_position(n): 
    positions = ['manager'] * int(n * 0.1) + ['cook'] * int(n * 0.3) + ['waiter'] * int(n * 0.7)
    random.shuffle(positions)
    return positions[:n]


# id_employees,firstname,surname,position,id_restaurant,salary,bonus_salary
n = 100
random_firstname = data_firstname(n)
random_surname = data_surname(n)
random_position = data_position(n)
random_id_rest = np.array([np.random.randint(1, 100) for _ in range(n)])
random_salary = np.array([np.random.randint(10_000, 100_000) for _ in range(n)])
random_bonus_salary = np.round(np.random.uniform(low=1000.0, high=10_000.0, size=n), 2)

with open('employees_new.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    header = ['id_employees', 'firstname', 'surname', 'position', 'id_restaurant', 'salary', 'bonus_salary']
    writer.writerow(header)
    for i in range(n):
        writer.writerow([i + 1,
                         random_firstname[i],
                         random_surname[i],
                         random_position[i], 
                         random_id_rest[i],
                         random_salary[i],
                         random_bonus_salary[i], 
                        ])