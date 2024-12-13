from Lab_5.common import *


def get_min_max_avg_salary(collection):
    return list(collection.aggregate(
        [
            {
                '$group': {
                    '_id': None,
                    'min_salary': {'$min': '$salary'},
                    'avg_salary': {'$avg': '$salary'},
                    'max_salary': {'$max': '$salary'}
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'min_salary': 1,
                    'avg_salary': {'$round': ['$avg_salary', 2]},
                    'max_salary': 1
                }
            }
        ]
    ))


def get_documents_for_professions(collection):
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


def get_salaries_by_cities(collection):
    return list(collection.aggregate(
        [
            {
                '$group': {
                    '_id': '$city',
                    'min_salary': {'$min': '$salary'},
                    'avg_salary': {'$avg': '$salary'},
                    'max_salary': {'$max': '$salary'}
                }
            },
            {
                '$project': {
                    'city': '$_id',
                    '_id': 0,
                    'min_salary': 1,
                    'avg_salary': {'$round': ['$avg_salary', 2]},
                    'max_salary': 1,
                }
            }
        ]
    ))


def get_salaries_by_jobs(collection):
    return list(collection.aggregate(
        [
            {
                '$group': {
                    '_id': '$job',
                    'min_salary': {'$min': '$salary'},
                    'avg_salary': {'$avg': '$salary'},
                    'max_salary': {'$max': '$salary'}
                }
            },
            {
                '$project': {
                    'job': '$_id',
                    '_id': 0,
                    'min_salary': 1,
                    'avg_salary': {'$round': ['$avg_salary', 2]},
                    'max_salary': 1,
                }
            }
        ]
    ))


def get_min_max_avg_age_by_cities(collection):
    return list(collection.aggregate(
        [
            {
                '$group': {
                    '_id': '$city',
                    'min_age': {'$min': '$age'},
                    'avg_age': {'$avg': '$age'},
                    'max_age': {'$max': '$age'}
                }
            },
            {
                '$project': {
                    'city': '$_id',
                    '_id': 0,
                    'min_age': 1,
                    'avg_age': {'$round': ['$avg_age', 2]},
                    'max_age': 1
                }
            }
        ]
    ))


def get_min_max_avg_age_by_jobs(collection):
    return list(collection.aggregate(
        [
            {
                '$group': {
                    '_id': '$job',
                    'min_age': {'$min': '$age'},
                    'avg_age': {'$avg': '$age'},
                    'max_age': {'$max': '$age'}
                }
            },
            {
                '$project': {
                    'job': '$_id',
                    '_id': 0,
                    'min_age': 1,
                    'avg_age': {'$round': ['$avg_age', 2]},
                    'max_age': 1
                }
            }
        ]
    ))


def get_max_salary_with_minimal_age(collection):
    return list(collection.aggregate(
        [
            {
                '$group': {
                    '_id': '$age',
                    'max_salary': {'$max': '$salary'}
                }
            },
            {
                '$sort': {'_id': 1}
            },
            {
                '$limit': 1
            },
            {
                '$project': {
                    'min_age': '$_id',
                    '_id': 0,
                    'max_salary': 1
                }
            }
        ]
    ))


def get_min_salary_with_maximal_age(collection):
    return list(collection.aggregate(
        [
            {
                '$group': {
                    '_id': '$age',
                    'min_salary': {'$min': '$salary'}
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
                    'min_age': '$_id',
                    '_id': 0,
                    'min_salary': 1
                }
            }
        ]
    ))


def age_by_cities_with_salary_gt_50k(collection):
    return list(collection.aggregate(
        [
            {
                '$match': {
                    'salary': {'$gt': 50000}
                }
            },
            {
                '$group': {
                    '_id': '$city',
                    'min_age': {'$min': '$age'},
                    'avg_age': {'$avg': '$age'},
                    'max_age': {'$max': '$age'}
                }
            },
            {
                '$sort': {'avg_age': -1}
            },
            {
                '$project': {
                    'city': '$_id',
                    '_id': 0,
                    'min_age': 1,
                    'avg_age': {'$round': ['$avg_age', 2]},
                    'max_age': 1
                }
            }
        ]
    ))


def salary_by_cities_and_professions_with_age(collection):
    return list(collection.aggregate(
        [
            {
                '$match': {
                    '$or':
                        [
                            {'age': {'$gt': 18, '$lt': 25}},
                            {'age': {'$gt': 50, '$lt': 65}}
                        ]
                    ,
                    'city': {'$in': ['Хельсинки', 'Варшава', 'Санкт-Петербург', 'Прага', 'Будапешт']},
                    'job': {'$in': ['Психолог', 'Бухгалтер', 'Водитель', 'Менеджер', 'Архитектор']}
                }
            },
            {
                '$group': {
                    '_id': {
                        'city': '$city',
                        'job': '$job'
                    },
                    'min_salary': {'$min': '$salary'},
                    'avg_salary': {'$avg': '$salary'},
                    'max_salary': {'$max': '$salary'}
                }
            },
            {
                '$project': {
                    'city': '$_id.city',
                    'job': '$_id.job',
                    '_id': 0,
                    'min_salary': 1,
                    'avg_salary': {'$round': ['$avg_salary', 2]},
                    'max_salary': 1
                }
            }
        ]
    ))


def salaries_of_professions_of_spb(collection):
    return list(collection.aggregate(
        [
            {
                '$match': {
                    'city': 'Санкт-Петербург',
                    'job': {'$in': ['Психолог', 'Бухгалтер', 'Водитель', 'Менеджер', 'Архитектор']}
                }
            },
            {
                '$group': {
                    '_id': {
                        'city': '$city',
                        'job': '$job'
                    },
                    'min_salary': {'$min': '$salary'},
                    'avg_salary': {'$avg': '$salary'},
                    'max_salary': {'$max': '$salary'}
                }
            },
            {
                '$sort': {'avg_salary': -1}
            },
            {
                '$project': {
                    'city': '$_id.city',
                    'job': '$_id.job',
                    '_id': 0,
                    'min_salary': 1,
                    'avg_salary': {'$round': ['$avg_salary', 2]},
                    'max_salary': 1
                }
            }
        ]
    ))


collection = connect_db()
collection.insert_many(parse_csv('../41/task_2_item.csv'))

save_data_as_json(get_min_max_avg_salary(collection)[0], 'get_min_max_avg_salary.json')
save_data_as_json(get_documents_for_professions(collection), 'get_documents_for_professions.json')
save_data_as_json(get_salaries_by_cities(collection), 'get_salaries_by_cities.json')
save_data_as_json(get_salaries_by_jobs(collection), 'get_salaries_by_jobs.json')
save_data_as_json(get_min_max_avg_age_by_cities(collection), 'get_min_max_avg_age_by_cities.json')
save_data_as_json(get_min_max_avg_age_by_jobs(collection), 'get_min_max_avg_age_by_jobs.json')
save_data_as_json(get_max_salary_with_minimal_age(collection), 'get_max_salary_with_minimal_age.json')
save_data_as_json(get_min_salary_with_maximal_age(collection), 'get_min_salary_with_maximal_age.json')
save_data_as_json(age_by_cities_with_salary_gt_50k(collection), 'age_by_cities_with_salary_gt_50k.json')
save_data_as_json(salary_by_cities_and_professions_with_age(collection), 'salary_by_cities_and_professions_with_age.json')
save_data_as_json(salaries_of_professions_of_spb(collection), 'salaries_of_professions_of_spb.json')
