from Lab_4.common import *
import msgpack
import csv


# artist;song;duration_ms;year;tempo;genre;energy;key;loudness
# Nelly;Air Force Ones;304000;2002;164.062;hip hop, pop, R&B;0.459;4;-9.74

def read_csv(file_path):
    songs = []
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            songs.append({
                "artist": row["artist"],
                "song": row["song"],
                "duration_ms": int(row["duration_ms"]),
                "year": int(row["year"]),
                "tempo": float(row["tempo"]),
                "genre": row["genre"],
                "energy": float(row["energy"]),
                "key": int(row["key"]),
                "loudness": float(row["loudness"])
            })
        return songs


def read_msgpack(file_path):
    with open(file_path, 'rb') as file:
        nodes = msgpack.load(file)
        return nodes


def process_songs(songs_pt_1, songs_pt_2):
    keys_of_pt_1 = set(songs_pt_1[0].keys())
    keys_of_pt_2 = set()
    keys_to_delete_from_pt_2 = set()
    for song_pt_2 in songs_pt_2:
        for song_pt_2_key in list(song_pt_2.keys()):
            if song_pt_2_key not in keys_of_pt_1:
                keys_to_delete_from_pt_2.add(song_pt_2_key)
                del song_pt_2[song_pt_2_key]
            else:
                keys_of_pt_2.add(song_pt_2_key)

    keys_to_delete_from_pt_1 = set()
    for song_pt_1 in songs_pt_1:
        for song_pt_1_key in list(song_pt_1.keys()):
            if song_pt_1_key not in keys_of_pt_2:
                keys_to_delete_from_pt_1.add(song_pt_1_key)
                del song_pt_1[song_pt_1_key]
            else:
                keys_of_pt_1.add(song_pt_1_key)

    print(keys_to_delete_from_pt_1)
    print(keys_to_delete_from_pt_2)

    print(keys_of_pt_1)
    print(keys_of_pt_2)

    print(keys_of_pt_1.difference(keys_to_delete_from_pt_1))
    print(keys_of_pt_2.difference(keys_to_delete_from_pt_2))


songs_part_1 = read_csv('../41/3/_part_1.csv')
songs_part_2 = read_msgpack('../41/3/_part_2.msgpack')

process_songs(songs_part_1, songs_part_2)

united_songs = songs_part_1 + songs_part_2


def create_songs_table(db):
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE songs (
        tempo TEXT,
        duration_ms INTEGER,
        genre TEXT,
        song TEXT,
        artist TEXT,
        year INTEGER
        )
    """)


def insert_songs_data_to_db(songs, db):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO songs (tempo, duration_ms, genre, song, artist, year)
        VALUES (:tempo, :duration_ms, :genre, :song, :artist, :year) 
    """, songs)
    db.commit()


def get_and_write_first_51_songs_sorted_by_tempo(db):
    cursor = db.cursor()
    db_nodes = cursor.execute("""
        SELECT *
        FROM songs
        ORDER BY tempo
        LIMIT 51
    """)

    songs = []
    for row in db_nodes.fetchall():
        songs.append(dict(row))
    write_data_to_json_file(songs, 'first_51_songs.json')


def get_and_write_duration_ms_stats(db):
    cursor = db.cursor()
    db_nodes = cursor.execute("""
        SELECT 
            SUM(duration_ms) as sum_duration_ms,
            MIN(duration_ms) as min_duration_ms,
            MAX(duration_ms) as max_duration_ms,
            ROUND(AVG(duration_ms), 2) as avg_duration_ms
        FROM songs
    """)

    stats = dict(db_nodes.fetchone())
    write_data_to_json_file(stats, 'songs_duration_ms_stats.json')


def get_and_write_artists(db):
    cursor = db.cursor()
    db_nodes = cursor.execute("""
        SELECT 
            artist,
            COUNT(*) as artist_count
        FROM songs
        GROUP BY artist
    """)

    artists = []
    for row in db_nodes.fetchall():
        artists.append(dict(row))
    write_data_to_json_file(artists, 'artists_stats.json')


def get_and_write_sorted_songs(db):
    cursor = db.cursor()
    db_nodes = cursor.execute("""
        SELECT * 
        FROM songs
        WHERE year > 2005
        ORDER BY year DESC
        LIMIT 56
    """)

    song_sorted_by_years = []
    for row in db_nodes.fetchall():
        song_sorted_by_years.append(dict(row))
    write_data_to_json_file(song_sorted_by_years, 'song_sorted_by_years.json')


db = connect_to_db('Task 3.db')
# create_songs_table(db)
# insert_songs_data_to_db(united_songs, db)

# query 1
get_and_write_first_51_songs_sorted_by_tempo(db)

# query 2
get_and_write_duration_ms_stats(db)

# query 3
get_and_write_artists(db)

# query 4
get_and_write_sorted_songs(db)
