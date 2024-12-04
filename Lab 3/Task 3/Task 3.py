import json
import math

from bs4 import BeautifulSoup

stars = []

# Будем считать показатели возраста звёзд
star_age_stats = {
    "max": -math.inf,
    "min": math.inf,
    "avg": 0,
    "sum": 0,
    "der": 0,
    "count": 0
}


def process_star_age_1(star_age, star_age_stats):
    star_age_stats['count'] += 1
    star_age_stats['sum'] += star_age
    if star_age > star_age_stats['max']:
        star_age_stats['max'] = star_age
    if star_age < star_age_stats['min']:
        star_age_stats['min'] = star_age


def process_star_age_2(stars, star_age_stats):
    star_age_stats['avg'] = star_age_stats['sum'] / star_age_stats['count']
    der_sum = 0
    for star in stars:
        star_age = star['age']
        der_sum += (star_age - star_age_stats['avg']) ** 2
    star_age_stats['der'] = math.sqrt(der_sum / (star_age_stats['count'] - 1))


# Будем считать статистику по спектральным классам звёзд
spectral_classes = {
    "total_count": 0
}


def process_spectral_class(spectral_class, spectral_classes):
    if spectral_class not in spectral_classes:
        spectral_classes[spectral_class] = {
            "freq": 0.0,
            "count": 1
        }
        spectral_classes['total_count'] += 1
    else:
        spectral_classes[spectral_class]['count'] += 1


def process_spectral_classes(spectral_classes):
    for spectral_class in spectral_classes:
        spectral_class = spectral_classes[spectral_class]
        if isinstance(spectral_class, dict):
            spectral_class['freq'] = spectral_class['count'] / spectral_classes['total_count']


def parse_xml_and_append(page_number, stars):
    int_props = {'radius'}
    float_props = {'rotation', 'age', 'distance', 'absolute-magnitude'}

    with open(f"../41/3/{page_number}.xml", encoding="utf-8") as file:
        xml_content = file.read()

    soup = BeautifulSoup(xml_content, "xml")
    star_xml = soup.star
    star = {}
    for el in star_xml:
        if el.name is None:
            continue
        if el.name in int_props:
            star[el.name] = int(el.get_text().strip())
        elif el.name in float_props:
            star[el.name] = float(el.get_text().strip().split(' ')[0])
            if el.name == 'age':
                process_star_age_1(star[el.name], star_age_stats)
        else:
            star[el.name] = el.get_text().strip()
            if el.name == 'spectral-class':
                process_spectral_class(star[el.name], spectral_classes)

    stars.append(star)


for i in range(1, 108):
    parse_xml_and_append(i, stars)

# Сортируем по созвездию
stars = sorted(stars, key=lambda star: star['constellation'])

# Оставляем только те, чей возраст >= 2 млрд. лет
filtered_stars = list(filter(lambda star: star['age'] >= 2, stars))

process_star_age_2(stars, star_age_stats)

process_spectral_classes(spectral_classes)

with open("res.json", "w", encoding="utf-8") as file:
    json.dump(stars, file, ensure_ascii=False)

with open("filtered_stars.json", "w", encoding="utf-8") as file:
    json.dump(filtered_stars, file, ensure_ascii=False)

with open("star_age_stats.json", "w", encoding="utf-8") as file:
    json.dump(star_age_stats, file, ensure_ascii=False)

with open("spectral_classes.json", "w", encoding="utf-8") as file:
    json.dump(spectral_classes, file, ensure_ascii=False)
