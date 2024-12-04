import json
import math

from bs4 import BeautifulSoup

# Будем считать показатели ёмкости аккумуляторов
acc_stats = {
    "max": -math.inf,
    "min": math.inf,
    "avg": 0,
    "sum": 0,
    "der": 0,
    "count": 0
}


def process_acc_1(acc, acc_stats):
    acc_stats['count'] += 1
    acc_stats['sum'] += acc
    if acc > acc_stats['max']:
        acc_stats['max'] = acc
    if acc < acc_stats['min']:
        acc_stats['min'] = acc


def process_acc_2(accs, acc_stats):
    acc_stats['avg'] = acc_stats['sum'] / acc_stats['count']
    der_sum = 0
    for item in accs:
        if 'acc' in item:
            acc = item['acc']
            der_sum += (acc - acc_stats['avg']) ** 2
    acc_stats['der'] = math.sqrt(der_sum / (acc_stats['count'] - 1))


# Будем считать статистику по типам матриц
matrix_types = {
    "total_count": 0
}


def process_matrix(matrix, matrix_types):
    if matrix not in matrix_types:
        matrix_types[matrix] = {
            "freq": 0.0,
            "count": 1
        }
        matrix_types['total_count'] += 1
    else:
        matrix_types[matrix]['count'] += 1


def process_matrix_types(matrix_types):
    for matrix_type in matrix_types:
        matrix = matrix_types[matrix_type]
        if isinstance(matrix, dict):
            matrix['freq'] = matrix['count'] / matrix_types['total_count']


def parse_html_and_append(page_number, items):
    int_props = {'ram', 'sim', 'camera', 'acc'}
    with open(f"../41/2/{page_number}.html", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    product_cards = soup.find_all("div", attrs={'class': 'pad'})
    for product_card in product_cards:
        item = {}
        item['id'] = int(product_card.a['data-id'])
        item['link'] = product_card.find_all('a')[1]['href']
        item['img'] = product_card.img['src']
        item['title'] = product_card.span.get_text().strip()
        item['price'] = float(product_card.price.get_text().strip().replace(' ₽', '').replace(' ', ''))
        item['bonus'] = int(product_card.strong.get_text().strip().split(' ')[2])

        properties = product_card.ul.find_all('li')
        for property in properties:
            item[property['type']] = property.get_text().strip()
            if property['type'] in int_props:
                item[property['type']] = int(property.get_text().strip().split(' ')[0])
            if property['type'] == 'acc':
                process_acc_1(item['acc'], acc_stats)
            if property['type'] == 'matrix':
                process_matrix(item[property['type']], matrix_types)

        items.append(item)


results = []
for i in range(1, 48):
    try:
        parse_html_and_append(i, results)
    except IndexError as ie:
        print(f"IndexError in file {i}.html")
        print(ie)

# print(results)

# Сортируем по id
results = sorted(results, key=lambda result: result['id'])

# Оставляем только те, за которые дают >= 4500 бонусов
filtered_results = list(filter(lambda result: result['bonus'] >= 4500, results))

process_acc_2(results, acc_stats)

process_matrix_types(matrix_types)

with open("res.json", "w", encoding="utf-8") as file:
    json.dump(results, file, ensure_ascii=False)

with open("filtered_res.json", "w", encoding="utf-8") as file:
    json.dump(filtered_results, file, ensure_ascii=False)

with open("acc_stats.json", "w", encoding="utf-8") as file:
    json.dump(acc_stats, file, ensure_ascii=False)

with open("matrix_stats.json", "w", encoding="utf-8") as file:
    json.dump(matrix_types, file, ensure_ascii=False)
