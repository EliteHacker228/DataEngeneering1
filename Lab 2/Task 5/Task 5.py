import csv
import json
import math
import pickle
import msgpack
import pandas as pd
import os

data = []
with open("dataset-mini.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        data.append({
            "List Year": int(row["List Year"]),
            "Town": row["Town"],
            "Assessed Value": float(row["Assessed Value"]),
            "Sale Amount": float(row["Sale Amount"]),
            "Sales Ratio": float(row["Sales Ratio"]),
            "Property Type": row["Property Type"],
            "Residential Type": row["Residential Type"],
        })

res = {}

str_fields = {"Town", "Property Type", "Residential Type"}
numeric_fields = {"List Year", "Assessed Value", "Sale Amount", "Sales Ratio"}

digit = {
    "max": 0,
    "min": 0,
    "avg": 0,
    "sum": 0,
    "der": 0,
    "count": 0
}

string = {
    "freq": 0.0,
    "count": 0
}

dataset_size = len(data)


def process_string_key(key, val):
    if key not in res:
        res[key] = {
            "count": 1
        }
    else:
        res[key]['count'] += 1

    if val not in res[key]:
        res[key][val] = {
            "freq": 0.0,
            "count": 1
        }
    else:
        res[key][val]['count'] += 1


def process_numeric_key(key, val):
    if key not in res:
        res[key] = {
            "max": val,
            "min": val,
            "avg": val,
            "sum": val,
            "der": val,
            "count": 1
        }
    else:
        res[key]['count'] += 1
        res[key]['sum'] += val
        if val > res[key]['max']:
            res[key]['max'] = val
        if val < res[key]['min']:
            res[key]['min'] = val


def process_node(node):
    for key in node:
        if node[key] not in res:
            if key in str_fields:
                process_string_key(key, node[key])
            if key in numeric_fields:
                process_numeric_key(key, node[key])


for node in data:
    process_node(node)

for res_key in res:
    if res_key in str_fields:
        for str_key in res[res_key]:
            if str_key == 'count':
                continue
            else:
                res[res_key][str_key]['freq'] = res[res_key][str_key]['count'] / res[res_key]['count']
    if res_key in numeric_fields:
        res[res_key]['avg'] = res[res_key]['sum'] / res[res_key]['count']

std_der_cumsums = {key: 0 for key in numeric_fields}

for node in data:
    for key in node:
        if key in numeric_fields:
            std_der_cumsums[key] += (node[key] - res[key]['avg']) ** 2

for key in std_der_cumsums:
    res[key]['der'] = math.sqrt(std_der_cumsums[key] / (res[key]['count'] - 1))

df = pd.read_json(json.dumps(res))
df.to_csv("res.csv", encoding="utf-8", index=False)

with open("res.json", "w", encoding="utf-8") as file:
    json.dump(res, file)

with open("res.msgpack", "wb") as file:
    msgpack.dump(res, file)

with open("res.pkl", "wb") as file:
    pickle.dump(res, file)

csv_size = os.path.getsize("res.csv")
json_size = os.path.getsize("res.json")
msgpack_size = os.path.getsize("res.msgpack")
pkl_size = os.path.getsize("res.pkl")

print(f"csv_size = {csv_size}")
print(f"json_size = {json_size}")
print(f"msgpack_size = {msgpack_size}")
print(f"pkl_size = {pkl_size}")
