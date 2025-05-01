import pandas as pd
import numpy as np

# Загружаем существующий файл заказов
df = pd.read_csv('order_new.csv', encoding='utf-8')

def total_amount():
    # Загружаем данные о блюдах в заказах и ценах
    dishes_order = pd.read_csv('dishes_order_new.csv')  # id_order, id_dishes, cnt_items
    dishes = pd.read_csv('dishes_new.csv')              # id_dishes, price
    
    # Объединяем таблицы
    merged = pd.merge(dishes_order, dishes, on='id_dishes', how='inner')
    
    # Вычисляем стоимость для каждой записи (цена × количество)
    merged['amount'] = merged['price'] * merged['cnt_items']
    
    # Группируем по id_order (а не id_dishes!)
    order_cost = round(merged.groupby('id_order')['amount'].sum().reset_index(),2)
    
    # Сопоставляем с исходным df, заполняя нули для заказов без блюд
    result = pd.merge(df[['id_order']], order_cost, on='id_order', how='left').fillna(0)
    
    return result['amount'].tolist()

# Присваиваем total_amount для всех строк df
df['total_amount'] = total_amount()

# Сохраняем изменения
df.to_csv('order_new.csv', index=False, encoding='utf-8')
print(df.head())
