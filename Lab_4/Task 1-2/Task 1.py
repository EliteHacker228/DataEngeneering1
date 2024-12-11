from Lab_4.common import *

# title, author, genre, pages, published_year, isbn, rating, views


def text_to_nodes(text):
    nodes = []
    splitter = '====='
    nodes_text = text.split(splitter)
    for node_text in nodes_text:
        if node_text.strip() == '':
            continue
        node = dict(line.split("::") for line in node_text.strip().split("\n"))
        node['pages'] = int(node['pages'])
        node['published_year'] = int(node['published_year'])
        node['rating'] = float(node['rating'])
        node['views'] = int(node['views'])
        nodes.append(node)
    return nodes


def parse_nodes_from_text_file(file_path):
    text = read_file(file_path)
    nodes = text_to_nodes(text)
    return nodes


def create_books_table(db):
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE books (
        title TEXT,
        author TEXT,
        genre TEXT,
        pages INTEGER,
        published_year INTEGER,
        isbn TEXT,
        rating REAL,
        views TEXT
        )
    """)


def insert_nodes_to_db(nodes, db):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO books (title, author, genre, pages, published_year, isbn, rating, views)
        VALUES (:title, :author, :genre, :pages, :published_year, :isbn, :rating, :views) 
    """, nodes)
    db.commit()


def get_and_write_first_51_books_sorted_by_pages(db):
    cursor = db.cursor()
    db_nodes = cursor.execute("""
        SELECT *
        FROM books
        ORDER BY pages
        LIMIT 51
    """)

    books = []
    for row in db_nodes.fetchall():
        books.append(dict(row))
    write_data_to_json_file(books, 'first_51_books.json')


def get_and_write_rating_stats(db):
    cursor = db.cursor()
    db_nodes = cursor.execute("""
        SELECT 
            SUM(rating) as sum_rating,
            MIN(rating) as min_rating,
            MAX(rating) as max_rating,
            ROUND(AVG(rating), 2) as avg_rating
        FROM books
    """)

    stats = dict(db_nodes.fetchone())
    write_data_to_json_file(stats, 'books_rating_stats.json')


def get_and_write_genres(db):
    cursor = db.cursor()
    db_nodes = cursor.execute("""
        SELECT 
            genre,
            COUNT(*) as books_of_genre_count
        FROM books
        GROUP BY genre
    """)

    genre_stats = []
    for row in db_nodes.fetchall():
        genre_stats.append(dict(row))
    write_data_to_json_file(genre_stats, 'genre_stats.json')


def get_and_write_sorted_books(db):
    cursor = db.cursor()
    db_nodes = cursor.execute("""
        SELECT * 
        FROM books
        WHERE rating > 0.4
        ORDER BY published_year DESC
        LIMIT 51
    """)

    genre_stats = []
    for row in db_nodes.fetchall():
        genre_stats.append(dict(row))
    write_data_to_json_file(genre_stats, 'sorted_books.json')


# STEP 1. Connect to db
db = connect_to_db('Task 1.db')

# STEP 2. Create table
# create_books_table(db)

# STEP 3. Insert data to table
# nodes = parse_nodes_from_text_file('../41/1-2/item.text')
# insert_nodes_to_db(nodes, db)

# query 1
get_and_write_first_51_books_sorted_by_pages(db)

# query 2
get_and_write_rating_stats(db)

# query 3
get_and_write_genres(db)

# query 4
get_and_write_sorted_books(db)
