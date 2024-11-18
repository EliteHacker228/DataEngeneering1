# Задание 6, вариант 41

from bs4 import BeautifulSoup
import requests

response = requests.get('https://rickandmortyapi.com/api/character/1')
json_object = response.json()

soup = BeautifulSoup("", "html.parser")

for property_name in json_object:
    print(property_name)
    print(json_object[property_name])


def json_to_html(json_obj):
    ul = BeautifulSoup('<ul></ul>', 'html.parser').ul

    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            li = BeautifulSoup(f'<li>{key}: </li>', 'html.parser').li
            li.append(json_to_html(value))
            ul.append(li)
    elif isinstance(json_obj, list):
        for item in json_obj:
            li = BeautifulSoup('<li></li>', 'html.parser').li
            li.append(json_to_html(item))
            ul.append(li)
    else:
        li = BeautifulSoup(f'<li>{json_obj}</li>', 'html.parser').li
        ul.append(li)

    return ul

def write_dict_as_csv(path, text):
    with open(path, "w", encoding="utf-8", newline="") as file:
        file.write(text)

write_dict_as_csv("sixth_task.html", str(json_to_html(json_object)))