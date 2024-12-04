import json
import math

from bs4 import BeautifulSoup

clothing_items = []

# Будем считать показатели рейтинга
clothes_rating_stats = {
    "max": -math.inf,
    "min": math.inf,
    "avg": 0,
    "sum": 0,
    "der": 0,
    "count": 0
}


def process_rating_1(cloth_rating, clothes_rating_stats):
    clothes_rating_stats['count'] += 1
    clothes_rating_stats['sum'] += cloth_rating
    if cloth_rating > clothes_rating_stats['max']:
        clothes_rating_stats['max'] = cloth_rating
    if cloth_rating < clothes_rating_stats['min']:
        clothes_rating_stats['min'] = cloth_rating


def process_rating_2(clothing_items, clothes_rating_stats):
    clothes_rating_stats['avg'] = clothes_rating_stats['sum'] / clothes_rating_stats['count']
    der_sum = 0
    for clothing_item in clothing_items:
        clothing_item_rating = clothing_item['rating']
        der_sum += (clothing_item_rating - clothes_rating_stats['avg']) ** 2
    clothes_rating_stats['der'] = math.sqrt(der_sum / (clothes_rating_stats['count'] - 1))


# Будем считать статистику по размерам одежды
clothing_sizes = {
    "total_count": 0
}


def process_clothing_size(clothing_size, clothing_sizes):
    if clothing_size not in clothing_sizes:
        clothing_sizes[clothing_size] = {
            "freq": 0.0,
            "count": 1
        }
        clothing_sizes['total_count'] += 1
    else:
        clothing_sizes[clothing_size]['count'] += 1


def process_clothing_sizes(clothing_sizes):
    for clothing_size in clothing_sizes:
        clothing_size = clothing_sizes[clothing_size]
        if isinstance(clothing_size, dict):
            clothing_size['freq'] = clothing_size['count'] / clothing_sizes['total_count']


def parse_xml_and_append(page_number, clothing_items):
    int_props = {'id', 'reviews'}
    float_props = {'price', 'rating'}
    bool_props = {'exclusive', 'sporty', 'new'}

    with open(f"../41/4/{page_number}.xml", encoding="utf-8") as file:
        xml_content = file.read()

    soup = BeautifulSoup(xml_content, "xml")
    for current_clothing_tag in soup.find_all('clothing'):
        clothing_item = {}
        for current_clothing_item in current_clothing_tag:
            if current_clothing_item.name is None:
                continue
            if current_clothing_item.name in int_props:
                clothing_item[current_clothing_item.name] = int(current_clothing_item.get_text())
            elif current_clothing_item.name in float_props:
                clothing_item[current_clothing_item.name] = float(current_clothing_item.get_text())
                if current_clothing_item.name == 'rating':
                    process_rating_1(clothing_item[current_clothing_item.name], clothes_rating_stats)
            elif current_clothing_item.name in bool_props:
                clothing_item[current_clothing_item.name] = (current_clothing_item.get_text() == "yes"
                                                             or current_clothing_item.get_text() == "+")
            else:
                clothing_item[current_clothing_item.name] = current_clothing_item.get_text().strip()
                if current_clothing_item.name == 'size':
                    process_clothing_size(clothing_item[current_clothing_item.name], clothing_sizes)
        clothing_items.append(clothing_item)


for i in range(1, 148):
    parse_xml_and_append(i, clothing_items)
# print(clothing_items)

# Оставляем только те, чья цена => 100000 и <= 250000
filtered_clothing_items = list(
    filter(lambda clothing_item: 100000 <= clothing_item['price'] <= 250000, clothing_items))

process_rating_2(clothing_items, clothes_rating_stats)

process_clothing_sizes(clothing_sizes)

with open("res.json", "w", encoding="utf-8") as file:
    json.dump(clothing_items, file, ensure_ascii=False)

with open("filtered_clothing_items.json", "w", encoding="utf-8") as file:
    json.dump(filtered_clothing_items, file, ensure_ascii=False)

with open("clothes_rating_stats.json", "w", encoding="utf-8") as file:
    json.dump(clothes_rating_stats, file, ensure_ascii=False)

with open("clothing_sizes.json", "w", encoding="utf-8") as file:
    json.dump(clothing_sizes, file, ensure_ascii=False)
