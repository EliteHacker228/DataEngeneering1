from Lab_5.common import *


def delete_by_predicate(collection):
    collection.delete_many(
        {
            '$or': [
                {'salary': {'$lt': 25000}},
                {'salary': {'$gt': 175000}}
            ]
        })


def increment_age(collection):
    collection.update_many(
        {},
        {
            '$inc': {'age': 1}
        })


def multiply_salaries_by_professions(collection):
    collection.update_many(
        {
            'job': {'$in': ['Водитель', 'Врач', 'Медсестра', 'Учитель']}
        },
        {
            '$mul': {'salary': 1.05}
        })


def multiply_salaries_by_cities(collection):
    collection.update_many(
        {
            'city': {'$in': ['Хельсинки', 'Варшава', 'Санкт-Петербург', 'Прага', 'Будапешт']}
        },
        {
            '$mul': {'salary': 1.07}
        })


def multiply_salaries_by_cities_and_jobs(collection):
    collection.update_many(
        {
            '$or': [
                {'age': {'$gt': 20, '$lte': 40}},
                {'age': {'$gt': 50, '$lt': 70}}
            ],
            'job': {'$in': ['Архитектор', 'Менеджер', 'Учитель']},
            'city': {'$in': ['Санкт-Петербург', 'Будапешт']}
        },
        {
            '$mul': {'salary': 1.10}
        })


def delete_by_custom_predicate(collection):
    collection.delete_many(
        {
            'city': 'Прага'
        })


collection = connect_db()
collection.insert_many(parse_msgpack('../41/task_3_item.msgpack'))

delete_by_predicate(collection)
increment_age(collection)
multiply_salaries_by_professions(collection)
multiply_salaries_by_cities(collection)
multiply_salaries_by_cities_and_jobs(collection)
delete_by_custom_predicate(collection)
