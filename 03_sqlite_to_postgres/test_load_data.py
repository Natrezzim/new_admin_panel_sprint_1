import sqlite3

import psycopg2
from psycopg2.extras import DictCursor

sqlite_conn = sqlite3.connect('db.sqlite')

pg_conn = psycopg2.connect(dbname='movies_database', user='app',
                           password='123qwe', host='127.0.0.1', port=5432)

cursor_sqlite = sqlite_conn.cursor()
cursor_postgresql = pg_conn.cursor()

cursor_sqlite.execute(
    'select id, title, description, creation_date, rating, type, created_at, updated_at from film_work')
filmsql3 = []
filmsql3 = cursor_sqlite.fetchall()
cursor_postgresql.execute(
    'select id, title, description, creation_date, rating, type, created, modified from content.film_work')
filmpg = cursor_postgresql.fetchall()


def test_film_work_row_count():
    count_of_rows_sqlite = cursor_sqlite.execute('select count(*) from film_work').fetchall()
    cursor_postgresql.execute('select count(*) from content.film_work')
    counts_of_rows_postgresql = cursor_postgresql.fetchall()
    assert counts_of_rows_postgresql == count_of_rows_sqlite


def test_genre_row_count():
    count_of_rows_sqlite = cursor_sqlite.execute('select count(*) from genre').fetchall()
    cursor_postgresql.execute('select count(*) from content.genre')
    counts_of_rows_postgresql = cursor_postgresql.fetchall()
    assert counts_of_rows_postgresql == count_of_rows_sqlite


def test_genre_film_work_row_count():
    count_of_rows_sqlite = cursor_sqlite.execute('select count(*) from genre_film_work').fetchall()
    cursor_postgresql.execute('select count(*) from content.genre_film_work')
    counts_of_rows_postgresql = cursor_postgresql.fetchall()
    assert counts_of_rows_postgresql == count_of_rows_sqlite


def test_person_row_count():
    count_of_rows_sqlite = cursor_sqlite.execute('select count(*) from person').fetchall()
    cursor_postgresql.execute('select count(*) from content.person')
    counts_of_rows_postgresql = cursor_postgresql.fetchall()
    assert counts_of_rows_postgresql == count_of_rows_sqlite


def test_person_film_work_row_count():
    count_of_rows_sqlite = cursor_sqlite.execute('select count(*) from person_film_work').fetchall()
    cursor_postgresql.execute('select count(*) from content.person_film_work')
    counts_of_rows_postgresql = cursor_postgresql.fetchall()
    assert counts_of_rows_postgresql == count_of_rows_sqlite
