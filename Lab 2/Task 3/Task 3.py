import json
import os

import msgpack


def read_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


products = read_json("../41/third_task.json")
products_stat = {}

for product in products:
    name = product['name']
    price = product['price']
    if name not in products_stat:
        products_stat[name] = {
            'name': name,
            'max_price': price,
            'avg_price': price,
            'count': 1,
            'min_price': price,
        }
    else:
        name = products_stat[name]
        if price > name['max_price']:
            name['max_price'] = price
        if price < name['min_price']:
            name['min_price'] = price
        name['avg_price'] += price
        name['count'] += 1

for name in products_stat:
    stat = products_stat[name]
    stat['avg_price'] /= stat['count']

to_save = list(products_stat.values())

with open("Task 3.json", "w", encoding="utf-8") as file:
    json.dump(to_save, file, ensure_ascii=False)

with open("Task 3.msgpack", "wb") as file:
    msgpack.dump(to_save, file)

json_size = os.path.getsize("Task 3.json")
msgpack_size = os.path.getsize("Task 3.msgpack")

print(f'json = {json_size}')
print(f'msgpack = {msgpack_size}')
print(f'diff = {json_size - msgpack_size}')