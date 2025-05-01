import pandas as pd
import csv
import numpy as np
from random import randint
import random
from datetime import time, timedelta, datetime

# id_order,id_customer(max=100),id_employees(100),id_restaurant(100),status,updated_at,payment_type,total_amount

def data_status(n):
    status_names = ['new', 'pending_payment', 'paid', 'preparing', 'ready', 'served', 'cancelled']
    return np.array(np.random.choice(status_names, size=n, replace=True))

def data_payment_type(n):
    probabilities = [0.35, 0.3, 0.2, 0.1, 0.05]
    types = ['cash', 'card', 'contactless', 'qr_code', 'loyalty_points']
    return np.array(np.random.choice(types, size=n, replace=True, p=probabilities))

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

def data_id_waiters():
    df = pd.read_csv('employees.csv', encoding='utf-8')
    waiters_ids = df[df['position'] == 'waiter']['id_employees'].to_numpy()
    return waiters_ids

n = 500
status = data_status(n)
payment_type = data_payment_type(n)
updated_at = data_time(n)
total_amount = [1 for _ in range(n)]
id_customer = np.array([np.random.randint(1, 101) for _ in range(n)])
id_employees = np.array(np.random.choice(data_id_waiters(), n, replace=True))
id_restaurant = np.array([np.random.randint(1, 101) for _ in range(n)])

with open('order_new.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    header = ['id_order', 'id_customer', 'id_employees', 'id_restaurant', 
                  'status', 'updated_at', 'payment_type', 'total_amount']
    writer.writerow(header)
    for i in range(n):
        writer.writerow([
            i + 1,
            id_customer[i],
            id_employees[i],
            id_restaurant[i],
            status[i],
            updated_at[i].strftime('%Y-%m-%d %H:%M:%S'),
            payment_type[i],
            total_amount[i]
        ])