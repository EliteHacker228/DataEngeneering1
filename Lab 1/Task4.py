# Задание 4, вариант 41
# Вариант 41
# 1. Удалите из таблицы столбец description
# 2. Найдите среднее арифметическое по столбцу quantity
# 3. Найдите максимум по столбцу rating
# 4. Найдите минимум по столбцу price
# 5. Отфильтруйте значения, взяв только те, status которых равен Backorder


import csv
import copy


def read_csv(path):
    data = []
    with open(path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append({
                "product_id": int(row["product_id"]),
                "name": row["name"],
                "price": float(row["price"]),
                "quantity": int(row["quantity"]),
                "category": row["category"],
                "description": row["description"],
                "production_date": row["production_date"],
                "expiration_date": row["expiration_date"],
                "rating": float(row["rating"]),
                "status": row["status"],
            })
        return data


def delete_description(data):
    data_copy = copy.deepcopy(data)
    for data_node in data_copy:
        del data_node["description"]
    return data_copy


def get_nodes_with_backorder_status(data):
    res = []
    for data_node in data:
        if data_node["status"] == "Backorder":
            res.append(data_node)
    return res


def middle_max_min(data):
    count = 0
    middle_cumsum = 0

    middle_quantity = 0
    max_rating = float('-inf')
    min_price = float('inf')
    for data_node in data:
        if float(data_node["rating"]) > max_rating:
            max_rating = float(data_node["rating"])

        if float(data_node['price']) < min_price:
            min_price = float(data_node["price"])

        count += 1
        middle_cumsum += data_node["quantity"]

    middle_quantity = middle_cumsum // count

    return {"middle_quantity": middle_quantity, "max_rating": max_rating, "min_price": min_price}


def write_dict_as_csv(path, nodes):
    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, nodes[0].keys())
        writer.writeheader()
        for row in nodes:
            writer.writerow(row)


data = read_csv("41/fourth_task.txt")

with_deleted_description = delete_description(data)
without_backorder = get_nodes_with_backorder_status(data)
middle_max_min = middle_max_min(data)
write_dict_as_csv("fourth_task_result__deleted_description.txt", with_deleted_description)
write_dict_as_csv("fourth_task_result__without_backorder.txt", without_backorder)
write_dict_as_csv("fourth_task_result__middle_max_min.txt", [middle_max_min])
