import json
import sqlite3


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        return text


def write_data_to_json_file(data, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)


def connect_to_db(file_path):
    connection = sqlite3.connect(file_path)
    connection.row_factory = sqlite3.Row
    return connection


def write_query_result_to_json(db_nodes, file_path):
    node = []
    for row in db_nodes.fetchall():
        node.append(dict(row))
    write_data_to_json_file(node, file_path)
