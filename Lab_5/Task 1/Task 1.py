import pymongo
from Lab_5.common import *


def sort_by_salary(collection):
    return list(collection.find({}, {'_id': False}, limit=10).sort({'salary': pymongo.DESCENDING}))


def find_by_age_sort_by_salary(collection):
    return list(collection
                .find({'age': {'$lt': 30}}, {'_id': False}, limit=15)
                .sort({'salary': pymongo.DESCENDING}))


def find_by_complex_predicate_sort_by_age(collection):
    return list(collection
                .find({'city': 'Будапешт',
                       'job': {'$in': ['Психолог', 'Архитектор', 'Учитель']}}, {'_id': False}, limit=10)
                .sort({'age': pymongo.ASCENDING}))


def count_by_complex_predicate(collection):
    return collection.count_documents({'age': {'$gte': 30, '$lte': 40},
                                       'year': {'$gte': 2019, '$lte': 2022},
                                       '$or': [
                                           {'salary': {'$gt': 50000, '$lte': 75000}},
                                           {'salary': {'$gt': 125000, '$lt': 150000}}
                                       ]})


collection = connect_db()
collection.insert_many(parse_txt('../41/task_1_item.text'))

save_data_as_json(sort_by_salary(collection), 'sort_by_salary.json')
save_data_as_json(find_by_age_sort_by_salary(collection), 'find_by_age_sort_by_salary.json')
save_data_as_json(find_by_complex_predicate_sort_by_age(collection), 'find_by_complex_predicate_by_sort_age.json')
save_data_as_json({'documents_by_complex_predicate': count_by_complex_predicate(collection)},
                  'count_by_complex_predicate.json')
