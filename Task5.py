# Задание 5, вариант 41
from bs4 import BeautifulSoup
import csv


def read_file(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def read_html_as_dict(html):
    soup = BeautifulSoup(html, "html.parser")
    columns = ["product_id", "name", "price", "quantity", "category", "description", "production_date",
               "expiration_date",
               "rating", "status"]

    to_float = ["price", "rating"]
    to_int = ["product_id", "quantity"]

    res = []
    for row in soup.find_all("tr"):
        cols = row.find_all("td")
        item = {}

        col_index = 0
        for col in cols:
            val = col.get_text(strip=True)
            val = val.replace(":", "")
            curr_col = columns[col_index]
            col_index += 1
            item[curr_col] = val

            if curr_col in to_float:
                item[curr_col] = float(val)
            if curr_col in to_int:
                item[curr_col] = int(val)
        if len(item) > 0:
            res.append(item)
    return res

def filter_dict(dict):
    res = []
    for node in dict:
        if node["product_id"] != 41:
            continue
        else:
            res.append(node)
    return res

def write_dict_as_csv(path, nodes):
    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, nodes[0].keys())
        writer.writeheader()
        for row in nodes:
            writer.writerow(row)

html = read_file("./41/fifth_task.html")
html_dict = read_html_as_dict(html)
filtered_html_dict = filter_dict(html_dict)
write_dict_as_csv("fifth_task_result__total.txt", html_dict)
write_dict_as_csv("fifth_task_result__41.txt", filtered_html_dict)