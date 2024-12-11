from Lab_4.common import *
import msgpack


def read_msgpack(file_path):
    with open(file_path, 'rb') as file:
        nodes = msgpack.load(file)
        return nodes


def create_books_editions_table(db):
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE books_editions (
        title TEXT,
        price INTEGER,
        place TEXT,
        date TEXT
        )
    """)


def insert_books_editions_data_to_db(books_editions, db):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO books_editions (title, price, place, date)
        VALUES (:title, :price, :place, :date) 
    """, books_editions)
    db.commit()


# Выводим всю информацию по дюне и её изданиям
def get_book_and_books_editions_for_dune(db):
    cursor = db.cursor()
    db_nodes = cursor.execute("""
        SELECT *
        FROM books as book
        JOIN books_editions AS books_edition ON book.title = books_edition.title
        WHERE book.title = 'Дюна'
    """)

    dune_editions = []
    for dune_edition in db_nodes.fetchall():
        dune_editions.append(dict(dune_edition))
    write_data_to_json_file(dune_editions, 'dune_editions.json')

# Выводим название книги, автора, дату выхода издания, и цену (и только для тех изданий, что дороже 2500)
def get_book_and_books_editions_prices(db):
    cursor = db.cursor()
    db_nodes = cursor.execute("""
        SELECT book.title, book.author, books_edition.date, books_edition.price
        FROM books as book
        JOIN books_editions AS books_edition ON book.title = books_edition.title
        WHERE book.title = '20 000 лье под водой' AND books_edition.price > 2500
    """)

    l20000_editions_prices = []
    for l20000_edition_prices in db_nodes.fetchall():
        l20000_editions_prices.append(dict(l20000_edition_prices))
    write_data_to_json_file(l20000_editions_prices, '2000_editions_prices.json')

# Выводим только романы (название и автор) и их рейтинг со средней ценой
def get_book_and_books_and_ratings_with_avg_price_by_genre(db):
    cursor = db.cursor()
    db_nodes = cursor.execute("""
        SELECT book.title, book.author, book.genre, book.rating, ROUND(AVG(books_edition.price), 2) as avg_price
        FROM books as book
        JOIN books_editions AS books_edition ON book.title = books_edition.title
        WHERE book.genre = 'фэнтези'
        GROUP BY book.title, book.author, book.genre, book.rating
    """)

    romans = []
    for roman in db_nodes.fetchall():
        romans.append(dict(roman))
    write_data_to_json_file(romans, 'fantasies_ratings_and_avg_price.json')


# STEP 1. Connect to db
db = connect_to_db('Task 1.db')

# STEP 2. Create table
# create_books_editions_table(db)

# STEP 3. Insert data to table
# books_editions = read_msgpack('../41/1-2/subitem.msgpack')
# insert_books_editions_data_to_db(books_editions, db)

# query 1
get_book_and_books_editions_prices(db)

# query 2
get_book_and_books_editions_prices(db)

# query 3
get_book_and_books_and_ratings_with_avg_price_by_genre(db)