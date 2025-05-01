import csv
from datetime import datetime, timedelta
import random
import pandas as pd

products = pd.read_csv('products.csv')
all_records = []

def check_overlap(id_product, from_dt, to_dt):
    for record in all_records:
        if record['id_products'] == id_product:
            record_from_dt = datetime.strptime(record['from_dt'], '%Y-%m-%d %H:%M:%S')
            record_to_dt = datetime.strptime(record['to_dt'], '%Y-%m-%d %H:%M:%S')
            if not (from_dt >= record_to_dt or to_dt <= record_from_dt):
                return True
    return False

def get_seasonal_factor(month):
    if month in [12, 1, 2]:
        return 1.2
    elif month in [6, 7, 8]:
        return 1.15
    else:
        return 1.0

end_date = datetime(2024, 1, 31, 9, 0, 0)

for _, product in products.iterrows():
    num_price_changes = random.randint(5, 12)  # Меньше изменений из-за ограничения
    first_from_dt = end_date - timedelta(days=random.randint(30, 365))
    first_from_dt = first_from_dt.replace(hour=9, minute=0, second=0, microsecond=0)
    
    base_price = round(random.uniform(10, 300), 2)
    current_price = base_price
    current_from_dt = first_from_dt
    
    for i in range(num_price_changes):
        if i == num_price_changes - 1:
            to_dt = end_date
        else:
            # Минимальный интервал 30 дней
            potential_to_dt = (current_from_dt + timedelta(days=random.randint(30, 60))).replace(hour=9, minute=0, second=0, microsecond=0)
            to_dt = min(potential_to_dt, end_date)
            while to_dt <= current_from_dt:
                to_dt += timedelta(days=30)
        
        while check_overlap(product['id_products'], current_from_dt, to_dt):
            current_from_dt = (to_dt + timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)
            if i == num_price_changes - 1:
                to_dt = end_date
            else:
                potential_to_dt = (current_from_dt + timedelta(days=random.randint(30, 60))).replace(hour=9, minute=0, second=0, microsecond=0)
                to_dt = min(potential_to_dt, end_date)
                while to_dt <= current_from_dt:
                    to_dt += timedelta(days=30)
        
        price_change = current_price * random.uniform(0.05, 0.10) * random.choice([1, -1])
        current_price = max(5, round(current_price + price_change, 2))
        seasonal_factor = get_seasonal_factor(current_from_dt.month)
        price = round(current_price * seasonal_factor, 2)
        
        record = {
            'id_products': product['id_products'],
            'name': product['name'],
            'price': price,
            'id_supplier': product['id_supplier'],
            'from_dt': current_from_dt.strftime('%Y-%m-%d %H:%M:%S'),
            'to_dt': to_dt.strftime('%Y-%m-%d %H:%M:%S')
        }
        all_records.append(record)
        current_from_dt = to_dt

all_records.sort(key=lambda x: (x['id_products'], x['from_dt']))

with open('history_products.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['id_products', 'name', 'price', 'id_supplier', 'from_dt', 'to_dt'])
    writer.writeheader()
    for record in all_records:
        writer.writerow(record)
