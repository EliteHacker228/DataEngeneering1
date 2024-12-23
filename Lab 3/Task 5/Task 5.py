import requests
from bs4 import BeautifulSoup
import json
import time
import re
import math

# Будем считать показатели цен
vargans_price_stats = {
    "max": -math.inf,
    "min": math.inf,
    "avg": 0,
    "sum": 0,
    "der": 0,
    "count": 0
}


def process_price_1(vargan_price, price_stats):
    price_stats['count'] += 1
    price_stats['sum'] += vargan_price
    if vargan_price > price_stats['max']:
        price_stats['max'] = vargan_price
    if vargan_price < price_stats['min']:
        price_stats['min'] = vargan_price


def process_price_2(vargans, vargans_prices_stats):
    vargans_prices_stats['avg'] = vargans_prices_stats['sum'] / vargans_prices_stats['count']
    der_sum = 0
    for vargan in vargans:
        vargan_price = vargan['price']
        der_sum += (vargan_price - vargans_prices_stats['avg']) ** 2
    vargans_prices_stats['der'] = math.sqrt(der_sum / (vargans_prices_stats['count'] - 1))


# Будем считать статистику по названиям
vargans_names_stats = {
    "total_count": 0
}


def write_to_json(data_to_write, file_name):
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(data_to_write, file, ensure_ascii=False)


def process_vargan_name(vargan_name, names_stats):
    if vargan_name not in names_stats:
        names_stats[vargan_name] = {
            "freq": 0.0,
            "count": 1
        }
        names_stats['total_count'] += 1
    else:
        names_stats[vargan_name]['count'] += 1


def process_vargan_names(vargans):
    for vargan in vargans:
        vargan_name = vargan['name']
        vargans_names_stats[vargan_name]['freq'] = vargans_names_stats[vargan_name]['count'] / vargans_names_stats[
            'total_count']


def pase_vargans_catalogue(url):
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')
        catalogue = soup.find_all('article')[1]
        cards = catalogue.find_all('div', class_='product-item__content')
        cards = cards[::2]
        vargans_catalogue = []
        for card in cards:
            # print(card)
            vargan = {}
            vargan['name'] = card.find('div', class_='product-item__link').get_text()
            vargan['img'] = 'https:' + card.find('img')['src']
            vargan['link'] = card.find('div', class_='product-item__link').find('a')['href']
            vargan['price'] = int(card.find('div', class_='product-item-price').get_text()
                                  .replace(' ₽', '')
                                  .replace(' ', ''))
            vargans_catalogue.append(vargan)

        return vargans_catalogue
    else:
        print("Ошибка при получении страницы:", response.status_code)


def handle_text(text, vargan):
    if 'длина' in text and ('варгана' in text or 'инструмента'):
        vargan['corpse_length'] = float(re.findall(r'\d+\.?\d*', text
                                                   .replace(' ', '')
                                                   .replace(',', '.'))[0])
    if 'размер' in text and 'корпуса' in text:
        vargan['corpse_width'] = float(re.findall(r'\d+\.?\d*', text
                                                  .replace(' ', '')
                                                  .replace(',', '.'))[0])
    if 'края' in text and 'язычка' in text:
        vargan['corpse_narrowest_part'] = float(re.findall(r'\d+\.?\d*', text
                                                           .replace(' ', '')
                                                           .replace(',', '.'))[1])
    if 'толщина' in text and 'корпуса' in text:
        vargan['corpse_thickness'] = float(re.findall(r'\d+\.?\d*', text
                                                      .replace(' ', '')
                                                      .replace(',', '.'))[0])
    if 'длина' in text and 'язычка' in text:
        vargan['tongue_length'] = float(re.findall(r'\d+\.?\d*', text
                                                   .replace(' ', '')
                                                   .replace(',', '.'))[0])
    if 'длина' in text and ('загиба' in text or 'колена' in text):
        vargan['tongue_curvedness'] = float(re.findall(r'\d+\.?\d*', text
                                                       .replace(' ', '')
                                                       .replace(',', '.'))[0])
    if 'вес' in text:
        vargan['weight'] = float(re.findall(r'\d+\.?\d*', text
                                            .replace(' ', '')
                                            .replace(',', '.'))[0])


def parse_vargan_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        vargan = {}
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')
        vargan['name'] = soup.find('div', class_='product__name show-for-medium').get_text().strip()
        process_vargan_name(vargan['name'], vargans_names_stats)
        vargan['link'] = url
        vargan['price'] = int(soup.find('span', class_='product-price-data').get_text())
        process_price_1(vargan['price'], vargans_price_stats)
        vargan['imgs'] = []
        for img in soup.find_all('img'):
            if img['src'].startswith('//i.siteapi.org'):
                vargan['imgs'].append('https:' + img['src'])
        description = soup.find('div', id='product-full-desc')
        ps = description.find_all('p')
        for p in ps:
            if p.get_text().count('•') > 1:
                for elem in p.get_text().split('•'):
                    handle_text(elem.lower(), vargan)
            else:
                handle_text(p.get_text().lower(), vargan)
        spans = description.find_all('span')
        for span in spans:
            handle_text(span.get_text().lower(), vargan)

        return vargan

    else:
        print("Ошибка при получении страницы:", response.status_code)


vargans_catalogue = pase_vargans_catalogue('https://vargan-ekb.ru/products/category/catalog-varganov')
write_to_json(vargans_catalogue, 'vargans_catalogue.json')

vargans = []
for vargan in vargans_catalogue:
    parsed_vargan = parse_vargan_page(vargan['link'])
    vargans.append(parsed_vargan)
    time.sleep(0.1)
    print(f"Parsed: {vargan['link']}")

# Сортируем варганы по весу, чтобы сначала вывести тяжёлые
vargans = sorted(vargans, key=lambda vargan: vargan['weight'], reverse=True)

# Оставляем только варганы дешевле 8000 руб
filtered_vargans = list(filter(lambda vargan: vargan['price'] < 8000, vargans))

process_vargan_names(vargans)
process_price_2(vargans, vargans_price_stats)

write_to_json(vargans, 'vargans.json')
write_to_json(filtered_vargans, 'filtered_vargans.json')
write_to_json(vargans_names_stats, 'vargans_names_stats.json')
write_to_json(vargans_price_stats, 'vargans_price_stats.json')
