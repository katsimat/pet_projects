import pandas as pd
import csv
import numpy as np
from random import randint
import random
from datetime import time, timedelta, datetime

def open_date(n):
    start_date = datetime(1900, 1, 1)
    random_dates = np.array([
        start_date + timedelta(days=np.random.randint(0, 365*120))
        for _ in range(n)
    ])
    return random_dates

def city_name(n):
    russian_cities = [
        "Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань", 
        "Нижний Новгород", "Челябинск", "Самара", "Омск", "Ростов-на-Дону",
        "Уфа", "Красноярск", "Воронеж", "Пермь", "Волгоград", "Краснодар",
        "Саратов", "Тюмень", "Тольятти", "Ижевск", "Барнаул", "Ульяновск",
        "Иркутск", "Хабаровск", "Ярославль", "Владивосток", "Махачкала",
        "Томск", "Оренбург", "Губкин", "Новокузнецк", "Рязань", "Астрахань",
        "Пенза", "Липецк", "Киров", "Чебоксары", "Тула", "Калининград",
        "Курск", "Ставрополь", "Магнитогорск", "Тверь", "Брянск", "Белгород",
        "Сургут", "Владимир", "Архангельск", "Калуга", "Смоленск", "Серпухов"
    ]
    cities = np.random.choice(russian_cities, size=n, replace=True)
    return cities


def open_times(n):
    return np.array([
        time(hour=np.random.randint(8, 14))
        for _ in range(n)
    ])

def rest_name(n):
    # Списки слов для генерации названий
    prefixes = ['Golden', 'Silver', 'Red', 'Blue', 'Green', 'Sunny', 'Cozy', 'Royal', 'Spicy', 'Fresh', 'Old', 'New']
    mains = ['Fork', 'Spoon', 'Plate', 'Table', 'Chef', 'Bistro', 'Grill', 'Tavern', 'Kitchen', 'House', 'Diner', 'Cafe']
    suffixes = ['Place', 'Spot', 'Haven', 'Nook', 'Lounge', 'Garden', 'Corner', '', '', '', '', '']  # Пустые для разнообразия

    # Генерация уникальных названий
    restaurants = set()
    while len(restaurants) < n:
        name = f"{random.choice(prefixes)} {random.choice(mains)} {random.choice(suffixes)}".strip()
        restaurants.add(name)

    # Преобразование в numpy-массив
    restaurants_array = np.array(list(restaurants))
    return restaurants_array


def street_name(n):
    street_types = ['Улица', 'Проспект', 'Дорога', 'Бульвар', 'Переулок', 'Проезд', 'Шоссе', 'Площадь']
    name_parts = [
    'Центральная', 'Московская', 'Ленинская', 'Советская', 'Мира', 'Садовая', 'Школьная', 'Заводская', 
    'Новая', 'Полевая', 'Лесная', 'Речная', 'Зелёная', 'Южная', 'Северная', 'Восточная', 'Западная', 
    'Пролетарская', 'Строителей', 'Молодёжная'
]
    # Генерация уникальных названий улиц
    streets = set()
    while len(streets) < n:
        name = f"{random.choice(name_parts)} {random.choice(street_types)}"
        streets.add(name)
    streets_array = np.array(list(streets))
    return streets_array

def close_time(opening_times):
    closing_times = np.array([
        # Преобразуем time в datetime для добавления интервала, затем обратно в time
        (datetime.combine(datetime.today(), ot) + timedelta(hours=np.random.randint(6, 10))).time()
        for ot in opening_times
    ])

    # Ограничение до 23:59
    closing_times = np.array([
        min(time(23, 59), ct, key=lambda t: (t.hour, t.minute))
        for ct in closing_times
    ])
    return closing_times

# Загрузка данных
data_dishes = pd.read_csv('dishes.csv')

target_dish_id = 123
target_cnt_rows = 500
n = 100
random_open_times = open_times(n)
random_rest = rest_name(n)
random_street = street_name(n)
random_close_times = close_time(random_open_times)
random_city = city_name(n)
random_house = np.array([np.random.randint(1, 100) for _ in range(n)])
random_markup = np.round(np.random.uniform(low=1.0, high=10.0, size=n), 2)
random_dates = open_date(n)
restaurant = [[] for _ in range(n)]
for i in range(n):
    rest_i = [i + 1,
              random_rest[i],
              random_dates[i],
              random_open_times[i],
              random_close_times[i],
              random_markup[i],
              random_city[i],
              random_street[i],
              random_house[i]]
    restaurant[i] = rest_i
print(restaurant[:5])

random_client_id = [randint(1, 1000) for _ in range(target_cnt_rows)]

with open('restaurant_new.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    header = ['id_restaurant', 'name', 'opening_date', 'open_time', 'close_time', 'markup', 'city', 'street', 'house']
    # Заголовок
    writer.writerow(header)
    # Данные
    for row in restaurant:
        writer.writerow([
            row[0],  # id
            str(row[1]),  # name
            row[2].strftime('%Y-%m-%d'),  # opening_date
            row[3].strftime('%H:%M'),  # open_time
            row[4].strftime('%H:%M'),  # close_time
            float(row[5]),  # markup
            str(row[6]),  # city
            str(row[7]),  # street
            int(row[8])  # house_number
        ])

