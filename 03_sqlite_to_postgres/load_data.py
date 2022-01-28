import datetime
import logging
import sqlite3
import uuid
from dataclasses import dataclass
from logging import info, warning

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

logging.basicConfig(level=logging.INFO)


@dataclass
class FilmWork(object):
    __slots__ = (
        'id',
        'title',
        'description',
        'creation_date',
        'rating',
        'type',
        'crated',
        'modified',
    )
    id: uuid.uuid4()
    title: str
    description: str
    creation_date: datetime.date
    rating: float
    type: str
    crated: datetime.datetime
    modified: datetime.datetime


@dataclass
class Genre(object):
    __slots__ = (
        'id',
        'name',
        'description',
        'created',
        'modified',
    )
    id: uuid.uuid4()
    name: str
    description: str
    created: datetime.datetime
    modified: datetime.datetime


@dataclass
class GenreFilmWork(object):
    __slots__ = (
        'id',
        'genre_id',
        'film_work_id',
        'created',
    )
    id: uuid.uuid4()
    genre_id: uuid.uuid4()
    film_work_id: uuid.uuid4()
    created: datetime.datetime


@dataclass
class Person(object):
    __slots__ = (
        'id',
        'full_name',
        'created',
        'modified',
    )
    id: uuid.uuid4()
    full_name: str
    created: datetime.datetime
    modified: datetime.datetime


@dataclass
class PersonFilmWork(object):
    __slots__ = (
        'id',
        'person_id',
        'film_work_id',
        'role',
        'created',
    )
    id: uuid.uuid4()
    person_id: uuid.uuid4()
    film_work_id: uuid.uuid4()
    role: str
    created: datetime.datetime


class SQLiteLoader(str):

    @staticmethod
    def load_movies():

        try:
            cursor = sqlite_conn.cursor()
        except sqlite3.Error as e:
            warning('SQlite connection error')
            warning(e)

        film_work = []

        select_from_film_work = "select id, title, description, creation_date, rating, type, created_at, updated_at from film_work"

        try:
            cursor.execute(select_from_film_work)
            info('Read from SQlite film_work table')
        except sqlite3.Error as e:
            warning('Read from SQlite film_work table error')
            warning(e)

        record = cursor.fetchall()
        for row in record:
            film_work.append(
                FilmWork(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                    row[6],
                    row[7])
            )

        genre = []
        select_from_genre = 'select id, name, description, created_at, updated_at from genre'
        try:
            cursor.execute(select_from_genre)
            info('Read from SQlite genre table')
        except sqlite3.Error as e:
            warning('Read from SQlite genre table error')
            warning(e)
        record = cursor.fetchall()
        for row in record:
            genre.append(
                Genre(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4]
                )
            )

        genre_film_work = []
        select_from_genre_film_work = 'select id, genre_id, film_work_id, created_at from genre_film_work'
        try:
            cursor.execute(select_from_genre_film_work)
            info('Read from SQlite genre_film_work table')
        except sqlite3.Error as e:
            warning('Read from SQlite genre_film_work table error')
            warning(e)
        record = cursor.fetchall()
        for row in record:
            genre_film_work.append(
                GenreFilmWork(
                    row[0],
                    row[1],
                    row[2],
                    row[3]
                )
            )

        person = []
        select_from_person = 'select id, full_name, created_at, updated_at from person'
        try:
            cursor.execute(select_from_person)
            info('Read from SQlite person table')
        except sqlite3.Error as e:
            warning('Read from SQlite person table error')
            warning(e)
        record = cursor.fetchall()
        for row in record:
            person.append(
                Person(
                    row[0],
                    row[1],
                    row[2],
                    row[3]
                )
            )

        person_film_work = []
        select_from_person_film_work = 'select id, person_id, film_work_id, role, created_at from person_film_work'
        try:
            cursor.execute(select_from_person_film_work)
            info('Read from SQlite person_film_work table')
        except sqlite3.Error as e:
            warning('Read from SQlite person_film_work table error')
            warning(e)
        record = cursor.fetchall()
        for row in record:
            person_film_work.append(
                PersonFilmWork(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4]
                )
            )

        cursor.close()

        data = {
            'film_work': [film_work],
            'genre': [genre],
            'genre_film_work': [genre_film_work],
            'person': [person],
            'person_film_work': [person_film_work]
        }

        cursor.close()

        return data


class PostgresSaver(str):

    @staticmethod
    def save_all_data(data):

        cursor = pg_conn.cursor()

        try:
            info('Write to PostgreSQL film_work table')
            for row in data.get('film_work'):
                for entry in row:
                    cursor.execute(
                        'insert into content.film_work (id, title, description, creation_date, rating, type, created, modified) values (%s, %s, %s, %s, %s, %s, %s, %s) on conflict do nothing',
                        (entry.id,
                         entry.title,
                         entry.description,
                         entry.creation_date,
                         entry.rating,
                         entry.type,
                         entry.crated,
                         entry.modified)
                    )
        except psycopg2.Error as e:
            warning('Write to PostgreSQL film_work table error')
            warning(e)

        try:
            info('Write to PostgreSQL genre table')
            for row in data.get('genre'):
                for entry in row:
                    cursor.execute(
                        'insert into content.genre (id, name, description, created, modified) values (%s, %s, %s, %s, %s) on conflict do nothing',
                        (entry.id,
                         entry.name,
                         entry.description,
                         entry.created,
                         entry.modified))
        except psycopg2.Error as e:
            warning('Write to PostgreSQL genre table error')
            warning(e)

        try:
            info('Write to PostgreSQL person table')
            for row in data.get('person'):
                for entry in row:
                    cursor.execute(
                        'insert into content.person (id, full_name, created, modified) values (%s, %s, %s, %s) on conflict do nothing',
                        (entry.id,
                         entry.full_name,
                         entry.created,
                         entry.modified))
        except psycopg2.Error as e:
            warning('Write to PostgreSQL person table error')
            warning(e)


        try:
            info('Write to PostgreSQL person_film_work table')
            for row in data.get('person_film_work'):
                print(len(row))
                for entry in row:
                    cursor.execute(
                        'insert into content.person_film_work (id, person_id, film_work_id, role, created) values (%s, %s, %s, %s, %s) on conflict do nothing',
                        (entry.id,
                         entry.person_id,
                         entry.film_work_id,
                         entry.role,
                         entry.created))

        except psycopg2.Error as e:
            warning('Write to PostgreSQL person_film_work table error')
            warning(e)
        try:
            info('Write to PostgreSQL genre_film_work table')
            for row in data.get('genre_film_work'):
                for entry in row:
                    cursor.execute(
                        'insert into content.genre_film_work (id, genre_id, film_work_id, created) values (%s, %s, %s, %s) on conflict do nothing',
                        (entry.id,
                         entry.genre_id,
                         entry.film_work_id,
                         entry.created))
        except psycopg2.Error as e:
            warning('Write to PostgreSQL genre_film_work table error')
            warning(e)


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres.

        Args:
              connection: connection to SQLite3
              pg_conn: connection to PostgreSQL

    @rtype: object
    @param connection: connection to SQLite3
    @param pg_conn: connection to PostgreSQL
    """
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    data_from_sql = sqlite_loader.load_movies()
    postgres_saver.save_all_data(data_from_sql)


if __name__ == '__main__':
    dsl = {
        'dbname': 'movies_database',
        'user': 'app',
        'password': '123qwe',
        'host': '127.0.0.1',
        'port': 5432,
    }
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        try:
            load_from_sqlite(sqlite_conn, pg_conn)
        except Exception as error:
            warning('load_from_sqlite method error')
            warning(error)
