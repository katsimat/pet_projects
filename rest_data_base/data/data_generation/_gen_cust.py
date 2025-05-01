import pandas as pd
import csv
import numpy as np
from random import randint
import random
from datetime import time, timedelta, datetime


def data_name(n):
    adjectives = ['Cool', 'Fast', 'Shy', 'Bright', 'Sly', 'Bold', 'Wild', 'Smart', 'Quiet', 'Dark']
    nouns = ['Cat', 'Wolf', 'Fox', 'Tiger', 'Bear', 'Hawk', 'Drake', 'Lynx', 'Owl', 'Crow']

    nicknames = []
    for _ in range(n):
        adj = random.choice(adjectives)
        noun = random.choice(nouns)
        nick = f"{adj}{noun}"
        nicknames.append(nick)
    return nicknames

def data_time(n):
    start_date = datetime(2010, 1, 1)
    end_date = datetime.now()

    registration_times = []
    for _ in range(n):
        # Случайная разница в днях и секундах
        days_diff = random.randint(0, (end_date - start_date).days)
        seconds_diff = random.randint(0, 86_399)  # Секунд в сутках - 1
        reg_time = start_date + timedelta(days=days_diff, seconds=seconds_diff)
        registration_times.append(reg_time)
    return registration_times

n = 100
random_name = data_name(n)
random_bonus = np.array([np.random.randint(1, 1000) for _ in range(n)])
random_registration_time = data_time(n)

with open('customer_new.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['id_customer', 'name', 'bonus', 'registration_time'])  # Заголовок
    for i in range(n):
        writer.writerow([
            i + 1,
            random_name[i],
            random_bonus[i],
            random_registration_time[i].strftime('%Y-%m-%d %H:%M:%S')
        ])

