from Lab_4.common import *
import pickle


def read_data_from_pkl(file_path):
    with open(file_path, 'rb') as file:
        pkl_products = pickle.load(file)
        return pkl_products


def preprocess_data(data):
    for node in data:
        if 'category' not in node:
            node['category'] = 'none'


def create_products_table(db):
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE products (
        name TEXT,
        price REAL,
        quantity INTEGER,
        category TEXT,
        fromCity TEXT,
        isAvailable INTEGER,
        views INTEGER,
        updates INTEGER default 0
        )
    """)


def insert_products_to_db(nodes, db):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO products (name, price, quantity, category, fromCity, isAvailable, views)
        VALUES (:name, :price, :quantity, :category, :fromCity, :isAvailable, :views) 
    """, nodes)
    db.commit()


def text_to_updates(text):
    updates = []
    splitter = '====='
    updates_text = text.split(splitter)
    for update_text in updates_text:
        if update_text.strip() == '':
            continue
        update = dict(line.split("::") for line in update_text.strip().split("\n"))
        if update['method'] == 'remove':
            update['param'] = None

        elif update['method'] in ['quantity_add', 'quantity_sub']:
            update['param'] = int(update['param'])

        elif update['method'] in ['price_abs', 'price_percent']:
            update['param'] = float(update['param'])

        elif update['method'] == 'available':
            update['param'] = int(bool(update['param']))

        updates.append(update)
    return updates


def parse_updates_from_text_file(file_path):
    text = read_file(file_path)
    nodes = text_to_updates(text)
    return nodes


def handle_remove(db, name):
    cursor = db.cursor()
    cursor.execute("DELETE FROM products WHERE name = ?", [name])
    db.commit()


def handle_price_abs_change(db, name, param):
    cursor = db.cursor()
    cursor.execute("""
        UPDATE products
        SET price = ROUND(price + ?, 2),
            updates = updates + 1 
        WHERE name = ?
    """, [param, name])
    db.commit()


def handle_price_percent_change(db, name, param):
    cursor = db.cursor()
    cursor.execute("""
        UPDATE products
        SET price = ROUND(price * (1 + ?), 2),
            updates = updates + 1 
        WHERE name = ?
    """, [param, name])
    db.commit()


def handle_quantity_change(db, name, param):
    cursor = db.cursor()
    cursor.execute("""
        UPDATE products
        SET quantity = quantity + ?,
            updates = updates + 1 
        WHERE name = ?
    """, [param, name])
    db.commit()


def handle_availability_change(db, name, param):
    cursor = db.cursor()
    cursor.execute("""
        UPDATE products
        SET isAvailable = ?,
            updates = updates + 1 
        WHERE name = ?
    """, [param, name])
    db.commit()


def apply_updates(db, updates):
    for update in updates:
        if update['method'] == 'remove':
            handle_remove(db, update['name'])

        elif update['method'] in ['quantity_add', 'quantity_sub']:
            handle_quantity_change(db, update['name'], update['param'])

        elif update['method'] == 'price_abs':
            handle_price_abs_change(db, update['name'], update['param'])

        elif update['method'] == 'price_percent':
            handle_price_percent_change(db, update['name'], update['param'])

        elif update['method'] == 'available':
            handle_availability_change(db, update['name'], update['param'])


# STEP 1. Connect to db
db = connect_to_db('Task 4.db')


# STEP 2. Create table
# create_products_table(db)

# STEP 3. Insert data to table
# products = read_data_from_pkl('../41/4/_product_data.pkl')
# preprocess_data(products)
# insert_products_to_db(products, db)

# STEP 4. Parse updates from txt file
# updates = parse_updates_from_text_file('../41/4/_update_data.text')

# STEP 5. Apply updates
# apply_updates(db, updates)

def top_10(db):
    cursor = db.cursor()
    db_nodes = cursor.execute("""
        SELECT * FROM products
        ORDER BY updates DESC
        LIMIT 10
    """)

    write_query_result_to_json(db_nodes, 'top_10_by_updates.json')


def groups_price_stats(db):
    cursor = db.cursor()
    db_nodes = cursor.execute("""
        SELECT 
        category as category,
        COUNT(*) as products_in_category_count,
        ROUND(SUM(price), 2)  as category_sum_price,
        ROUND(MIN(price), 2)  as category_min_price,
        ROUND(MAX(price), 2)  as category_max_price,
        ROUND(AVG(price), 2)  as category_avg_price
        FROM products
        GROUP BY category
    """)

    write_query_result_to_json(db_nodes, 'price_stats_by_groups.json')


def groups_leftovers_stats(db):
    cursor = db.cursor()
    db_nodes = cursor.execute("""
        SELECT 
        category as category,
        COUNT(*) as products_in_category_count,
        SUM(quantity)  as category_quantity_sum,
        MIN(quantity)  as category_quantity_min,
        MAX(quantity)  as category_quantity_max,
        ROUND(AVG(quantity), 2)  as category_quantity_avg
        FROM products
        GROUP BY category
    """)

    write_query_result_to_json(db_nodes, 'leftovers_stats_by_groups.json')


def groups_quantity_by_cities(db):
    cursor = db.cursor()
    db_nodes = cursor.execute("""
        SELECT 
        fromCity as city,
        quantity as quantity
        FROM products
        GROUP BY fromCity
        ORDER BY quantity DESC
    """)

    write_query_result_to_json(db_nodes, 'products_quantities_by_cities.json')


# STEP 6. Вывести топ-10 самых обновляемых товаров
top_10(db)

# STEP 7. Проанализировать цены товаров, найдя (сумму, мин, макс, среднее) для каждой группы, а также количество товаров в группе
groups_price_stats(db)

# STEP 8. Проанализировать остатки товаров, найдя (сумму, мин, макс, среднее) для каждой группы товаров
groups_leftovers_stats(db)

# STEP 9. Произвольный запрос (смотрим, в каком городе больше всего товаров)
groups_quantity_by_cities(db)
