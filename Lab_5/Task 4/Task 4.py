from Lab_5.common import *
import pymongo

collection = connect_db_task4()


collection.insert_many(parse_msgpack('dataset/bank-full_pt1.msgpack'))
collection.insert_many(parse_json('dataset/bank-full_pt2.json'))


def sort_by_balance(collection):
    return list(collection
                .find({}, {'_id': False}, limit=30)
                .sort({'balance': pymongo.DESCENDING}))


def find_by_martial_status_sort_by_duration(collection):
    return list(collection
                .find({'marital': 'married'}, {'_id': False}, limit=30)
                .sort({'duration': pymongo.DESCENDING}))


def find_first_30_by_result(collection):
    return list(collection
                .find({'y': 'yes'}, {'_id': False}, limit=30))


def count_by_positive_result(collection):
    return collection.count_documents({'y': 'yes'})


def count_by_education(collection):
    return collection.count_documents({'education': 'primary'})


def get_min_max_avg_balance(collection):
    return list(collection.aggregate(
        [
            {
                '$group': {
                    '_id': None,
                    'min_balance': {'$min': '$balance'},
                    'avg_balance': {'$avg': '$balance'},
                    'max_balance': {'$max': '$balance'}
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'min_balance': 1,
                    'avg_balance': {'$round': ['$avg_balance', 2]},
                    'max_balance': 1
                }
            }
        ]
    ))


def get_documents_for_jobs(collection):
    return list(collection.aggregate(
        [
            {
                '$group': {
                    '_id': '$job',
                    'count': {'$sum': 1}
                }
            },
            {
                '$project': {
                    'job': '$_id',
                    '_id': 0,
                    'count': 1,
                }
            }
        ]
    ))


def get_balance_by_education(collection):
    return list(collection.aggregate(
        [
            {
                '$group': {
                    '_id': '$education',
                    'min_balance': {'$min': '$balance'},
                    'avg_balance': {'$avg': '$balance'},
                    'max_balance': {'$max': '$balance'}
                }
            },
            {
                '$project': {
                    'city': '$_id',
                    '_id': 0,
                    'min_balance': 1,
                    'avg_balance': {'$round': ['$avg_balance', 2]},
                    'max_balance': 1,
                }
            }
        ]
    ))


def get_verdict_by_martial(collection):
    return list(collection.aggregate(
        [
            {
                '$group': {
                    '_id': '$marital',
                    'count': {'$sum': 1}
                }
            },
            {
                '$project': {
                    'job': '$_id',
                    '_id': 0,
                    'count': 1,
                }
            }
        ]
    ))


def get_max_age_with_minimal_duration_and_y_verdict(collection):
    return list(collection.aggregate(
        [
            {
                '$match': {
                    'y': 'yes'
                }
            },
            {
                '$group': {
                    '_id': '$age',
                    'min_duration': {'$min': '$duration'},
                    'y': {'$first': '$y'}
                }
            },
            {
                '$sort': {'_id': -1}
            },
            {
                '$limit': 1
            },
            {
                '$project': {
                    'max_age': '$_id',
                    '_id': 0,
                    'y': 1,
                    'min_duration': 1
                }
            }
        ]
    ))


def delete_by_predicate(collection):
    collection.delete_many(
        {
            'balance': {'$gt': 20000}
        })


def increment_balance(collection):
    collection.update_many(
        {},
        {
            '$inc': {'balance': 5000}
        })


def multiply_balance_by_education(collection):
    collection.update_many(
        {
            'education': {'$in': ['secondary', 'primary']}
        },
        {
            '$mul': {'balance': 1.5}
        })


def reduce_balance_by_loan(collection):
    collection.update_many(
        {
            'loan': 'yes'
        },
        {
            '$mul': {'balance': 0.9}
        })


def reduce_duration_by_outcome(collection):
    collection.update_many(
        {
            'y': 'yes'
        },
        {
            '$mul': {'balance': 1.1}
        })


save_data_as_json(sort_by_balance(collection), 'subtask_1/sort_by_balance.json')
save_data_as_json(find_by_martial_status_sort_by_duration(collection),
                  'subtask_1/find_by_martial_status_sort_by_duration.json')
save_data_as_json(find_first_30_by_result(collection), 'subtask_1/find_first_30_by_result.json')
save_data_as_json({'persons_subscribed_for_a_deposit': count_by_positive_result(collection)},
                  'subtask_1/persons_subscribed_for_a_deposit.json')
save_data_as_json({'persons_with_primary_education': count_by_education(collection)},
                  'subtask_1/persons_with_primary_education.json')

save_data_as_json(get_min_max_avg_balance(collection), 'subtask_2/min_max_avg_balance.json')
save_data_as_json(get_documents_for_jobs(collection), 'subtask_2/documents_for_jobs.json')
save_data_as_json(get_balance_by_education(collection), 'subtask_2/balance_by_education.json')
save_data_as_json(get_verdict_by_martial(collection), 'subtask_2/get_verdict_by_martial.json')
save_data_as_json(get_max_age_with_minimal_duration_and_y_verdict(collection),
                  'subtask_2/max_age_with_minimal_duration_and_y_verdict.json')

delete_by_predicate(collection)
increment_balance(collection)
multiply_balance_by_education(collection)
reduce_balance_by_loan(collection)
reduce_duration_by_outcome(collection)
