from Lab_4.common import *
import csv
import json


# Предметная область: административная деятельность, учёт личных транспортных средств
# Описание: электрические и гибридные автомобили, зарегистрированные в штате Вашингтон


def read_dataset_from_json(file_path):
    return json.loads(read_file(file_path))


def read_dataset_from_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        res = []
        for data in reader:
            for key in list(data):
                if key in ['Postal Code', 'Model Year', 'Electric Range', 'Base MSRP', 'Legislative District',
                           'DOL Vehicle ID', '2020 Census Tract']:
                    data[key] = int(data[key])
            res.append(data)
        return res


dataset_pt_1 = read_dataset_from_json('dataset_pt_1.json')
dataset_pt_2 = read_dataset_from_csv('dataset_pt_2.csv')

dataset = dataset_pt_1 + dataset_pt_2


def create_tables(db):
    cursor = db.cursor()

    cursor.execute("""
            CREATE TABLE vehicle_geo (
            vin TEXT,
            country TEXT,
            city TEXT,
            state TEXT,
            postal_code INTEGER,
            vehicle_location TEXT
            )
        """)

    cursor.execute("""
            CREATE TABLE vehicle_specs (
            vin TEXT,
            make TEXT,
            model TEXT,
            electric_vehicle_data TEXT,
            cafv TEXT,
            electric_utility TEXT,
            electric_range INTEGER,
            base_msrp INTEGER
            )
        """)

    cursor.execute("""
            CREATE TABLE vehicle_registration (
            vin TEXT,
            legislative_district INTEGER,
            dol_id INTEGER,
            census_2020 INTEGER
            )
        """)


def insert_data_into_db(dataset, db):
    cursor = db.cursor()

    vehicle_geo_data = [(
        vehicle["VIN (1-10)"],
        vehicle["County"],
        vehicle["City"],
        vehicle["State"],
        vehicle["Postal Code"],
        vehicle["Vehicle Location"]
    ) for vehicle in dataset]

    cursor.executemany("""
        INSERT INTO vehicle_geo (vin, country, city, state, postal_code, vehicle_location)
        VALUES (?, ?, ?, ?, ?, ?) 
    """, vehicle_geo_data)

    vehicle_specs_data = [(
        vehicle["VIN (1-10)"],
        vehicle["Make"],
        vehicle["Model"],
        vehicle["Electric Vehicle Type"],
        vehicle["Clean Alternative Fuel Vehicle (CAFV) Eligibility"],
        vehicle["Electric Utility"],
        vehicle["Electric Range"],
        vehicle["Base MSRP"]
    ) for vehicle in dataset]

    cursor.executemany("""
        INSERT INTO vehicle_specs (vin, make, model, electric_vehicle_data, cafv, electric_utility, electric_range, base_msrp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?) 
    """, vehicle_specs_data)

    vehicle_registration_data = [(
        vehicle["VIN (1-10)"],
        vehicle["Legislative District"],
        vehicle["DOL Vehicle ID"],
        vehicle["2020 Census Tract"]
    ) for vehicle in dataset]

    cursor.executemany("""
        INSERT INTO vehicle_registration (vin, legislative_district, dol_id, census_2020)
        VALUES (?, ?, ?, ?) 
    """, vehicle_registration_data)

    db.commit()


# Вывести количество автомобилей марки subaru в каждом городе
def get_subaru_by_cities(db):
    cursor = db.cursor()
    db_nodes = cursor.execute("""
        SELECT 
        vg.city AS city,
        COUNT(*) AS subaru_number
        FROM vehicle_specs AS vs
        JOIN vehicle_geo AS vg ON vs.vin = vg.vin
        WHERE vs.make = 'SUBARU' 
        GROUP BY vg.city
        ORDER BY subaru_number DESC
    """)

    write_query_result_to_json(db_nodes, "subaru_by_cities.json")


# Вывести данные по городам о всех автомобилях в округе Jefferson
def get_vancouver_cars(db):
    cursor = db.cursor()
    db_nodes = cursor.execute("""
        SELECT
        vg.country AS country,
        vg.city AS city,
        vs.make AS make,
        vs.model AS model,
        COUNT(*) AS models_num
        FROM vehicle_geo AS vg
        JOIN vehicle_specs AS vs ON vg.vin = vs.vin
        WHERE vg.country = 'Jefferson'
        GROUP BY model, make, city
    """)

    write_query_result_to_json(db_nodes, "jefferson_cars.json")


# Вывести марку, модель, тип силовой установки и дальность для всех автомобилей с дальностью > 20
def cars_by_er(db):
    cursor = db.cursor()
    db_nodes = cursor.execute("""
        SELECT
        make, model, electric_vehicle_data, electric_range
        FROM vehicle_specs
        WHERE electric_range > 20
        GROUP BY model
        ORDER BY electric_range DESC
    """)

    write_query_result_to_json(db_nodes, "cars_by_er.json")


# Вывести число автомобилей по модели, которые являются абонентами "PUGET SOUND ENERGY INC"
def get_pse_abonents(db):
    cursor = db.cursor()
    db_nodes = cursor.execute("""
        SELECT
        make, model, electric_utility, COUNT(*) AS count
        FROM vehicle_specs
        WHERE electric_utility > 'PUGET SOUND ENERGY INC'
        GROUP BY model
        ORDER BY count DESC
    """)

    write_query_result_to_json(db_nodes, "psei_abonents.json")


# Вывести по vin число городов, в которых был зарегистрирован автомобиль, марку и модель автомобиля
# VIN может дублироваться в рамках одной таблицы vehicle_specs и vehicle_geo, город может дублироваться в рамках
# одной таблицы vehicle_geo, поэтому делаем JOIN геозаписей с данными о машинах через выбор уникальных записей (DISTINCT) 
def get_cities_by_vin(db):
    cursor = db.cursor()
    db_nodes = cursor.execute("""
        SELECT vs.vin, vs.make, vs.model, COUNT(vg.city) AS cities_count
        FROM vehicle_geo AS vg
        JOIN (
            SELECT DISTINCT vin, make, model
            FROM vehicle_specs
        ) AS vs ON vs.vin=vg.vin
        GROUP BY vs.vin, vs.make, vs.model, vg.city
        ORDER BY COUNT(vg.city) DESC
    """)

    write_query_result_to_json(db_nodes, "cities_by_vin.json")


# Вывести среднюю дальность для каждой марки
def get_avg_range_by_makes(db):
    cursor = db.cursor()
    db_nodes = cursor.execute("""
        SELECT make, ROUND(AVG(electric_range), 2) as avg_electric_range
        FROM vehicle_specs
        GROUP BY make
        ORDER BY AVG(electric_range) DESC
    """)

    write_query_result_to_json(db_nodes, "get_avg_range_by_makes.json")


db = connect_to_db('Task 5.db')

# STEP 1. Создать таблицы
# create_tables(db)

# STEP 2. Заполнить таблицы
# insert_data_into_db(dataset, db)

# query 1
get_subaru_by_cities(db)

# query 2
get_vancouver_cars(db)

# query 3
cars_by_er(db)

# query 4
get_pse_abonents(db)

# query 5
get_cities_by_vin(db)

# query 6
get_avg_range_by_makes(db)
