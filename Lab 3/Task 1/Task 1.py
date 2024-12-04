import json
import math

from bs4 import BeautifulSoup

# Будем считать показатели цены
price_stats = {
    "max": -math.inf,
    "min": math.inf,
    "avg": 0,
    "sum": 0,
    "der": 0,
    "count": 0
}


def process_price_1(price, price_stats):
    price_stats['count'] += 1
    price_stats['sum'] += price
    if price > price_stats['max']:
        price_stats['max'] = price
    if price < price_stats['min']:
        price_stats['min'] = price


def process_price_2(items, price_stats):
    price_stats['avg'] = price_stats['sum'] / price_stats['count']
    der_sum = 0
    for item in items:
        price = item['price']
        der_sum += (price - price_stats['avg']) ** 2
    price_stats['der'] = math.sqrt(der_sum / (price_stats['count'] - 1))


# Будем считать статистику по городам
cities = {
    "total_count": 0
}


def process_city(city, cities):
    if city not in cities:
        cities[city] = {
            "freq": 0.0,
            "count": 1
        }
        cities['total_count'] += 1
    else:
        cities[city]['count'] += 1


def process_cities(cities):
    for city_name in cities:
        city = cities[city_name]
        if isinstance(city, dict):
            city['freq'] = city['count'] / cities['total_count']


def parse_html(page_number):
    with open(f"../41/1/{page_number}.html", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    product_card = soup.find_all("div", attrs={'class': 'product-wrapper'})[0]
    item = {}
    spans = product_card.find_all('span')
    temp_spans_text = spans[0].get_text().replace('\n', '').replace('Наличие:', ';Наличие:').split(';')
    item['article_number'] = temp_spans_text[0].split('Артикул:')[1].strip()
    item['in_stock'] = temp_spans_text[1].split('Наличие:')[1].strip() == 'Да'
    h1s = product_card.find_all('h1')
    item['name'] = h1s[0].get_text().replace('\n', '').split('Название:')[1].strip()
    ps = product_card.find_all('p')
    temp_ps_text = ps[0].get_text().replace('\n', '').replace('Цена:', ';Цена:').split(';')
    item['city'] = temp_ps_text[0].split('Город:')[1].strip()
    process_city(item['city'], cities)
    item['price'] = float(temp_ps_text[1].split('Цена:')[1].strip().replace(' руб', ''))
    process_price_1(item['price'], price_stats)
    item['information'] = {}
    item['information']['color'] = spans[1].get_text().strip().split('\n')[0].split(': ')[1]
    item['information']['amount'] = int(spans[2].get_text().strip().split('\n')[0].split(': ')[1].replace(' шт', ''))
    item['information']['dimensions'] = spans[3].get_text().strip().split(':')[1]
    item['rating'] = float(spans[4].get_text().strip().split(': ')[1])
    item['views'] = int(spans[5].get_text().strip().split(': ')[1])

    return item


results = []
for i in range(2, 64):
    results.append(parse_html(i))

# Сортируем по рейтингу
results = sorted(results, key=lambda result: result['rating'], reverse=True)

# Оставляем только те, что в наличии
filtered_results = list(filter(lambda result: result['in_stock'], results))

# Рассчитываем статистические характеристики для цены
process_price_2(results, price_stats)

# Рассчитываем характеристики строкового поля
process_cities(cities)

with open("res.json", "w", encoding="utf-8") as file:
    json.dump(results, file, ensure_ascii=False)

with open("filtered_res.json", "w", encoding="utf-8") as file:
    json.dump(filtered_results, file, ensure_ascii=False)

with open("price_stats.json", "w", encoding="utf-8") as file:
    json.dump(price_stats, file, ensure_ascii=False)

with open("cities_stats.json", "w", encoding="utf-8") as file:
    json.dump(cities, file, ensure_ascii=False)
