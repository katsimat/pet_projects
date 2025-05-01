import pandas as pd
import csv
import numpy as np
from random import randint
import random
from datetime import time, timedelta, datetime

def data_company_names(n):
    adjectives = ['Swift', 'Bright', 'Golden', 'Silent', 'Prime', 'Dynamic', 'Clear', 'Bold', 'Fresh', 'Elite']
    nouns = ['Solutions', 'Group', 'Tech', 'Foods', 'Enterprises', 'Systems', 'Co', 'Partners', 'Labs', 'Works']
    return [f"{random.choice(adjectives)}{random.choice(nouns)}" for _ in range(n)]

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

#id_supplier,name,city,street,house,quality_assessment
n = 100
name = data_company_names(n)
city = city_name(n)
street = street_name(n)
house = np.array([np.random.randint(1, 100) for _ in range(n)])
quality_assessment = np.round(np.random.uniform(low=1.0, high=10.0, size=n), 2)


with open('supplier_new.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    header = ['id_supplier', 'name', 'city', 'street', 'house', 'quality_assessment']
    writer.writerow(header)
    for i in range(n):
        writer.writerow([i + 1,
                         name[i],
                         city[i],
                         street[i], 
                         house[i],
                         quality_assessment[i] 
                        ])