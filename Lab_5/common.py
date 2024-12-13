import msgpack
from pymongo import MongoClient
import csv
import json


def connect_db():
    client = MongoClient()
    db = client["db-2024"]
    return db.jobs


def connect_db_task4():
    client = MongoClient()
    db = client["db-2024"]
    return db.banking


def parse_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        text_nodes = text.split('=====')[0:-1]
        int_fields = ['salary', 'id', 'year', 'age']
        nodes = []
        for node in text_nodes:
            nodes_fvs = node.strip().split('\n')
            node = {}
            for node_fv in nodes_fvs:
                [node_field, node_value] = node_fv.split('::')
                if node_field in int_fields:
                    node_value = int(node_value)
                node[node_field] = node_value
            nodes.append(node)
        return nodes


def parse_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        int_fields = ['salary', 'id', 'year', 'age']
        nodes = []
        for row in reader:
            node = {}
            for key in row:
                node[key] = row[key]
                if key in int_fields:
                    node[key] = int(node[key])
            nodes.append(node)
        return nodes


def parse_msgpack(file_path):
    with open(file_path, 'rb') as file:
        nodes = msgpack.load(file)
        return nodes


def parse_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        nodes = json.load(file)
        return nodes


def save_data_as_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)
