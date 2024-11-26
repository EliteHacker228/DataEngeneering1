import pickle
import json

with open('../41/fourth_task_products.json', 'rb') as file:
    products = pickle.load(file)

with open('../41/fourth_task_updates.json', 'r', encoding='utf-8') as file:
    updates = json.load(file)

product_map = {}

methods = {
    'add': lambda price, param: price + param,
    'sub': lambda price, param: price - param,
    'percent+': lambda price, param: price * (1 + param),
    'percent-': lambda price, param: price * (1 - param),
}

for product in products:
    product_map[product['name']] = product

for update in updates:
    product = product_map[update['name']]
    product['price'] = methods[update['method']](product['price'], update['param'])

with open("Task 4.pkl", "wb") as file:
    pickle.dump(products, file)
