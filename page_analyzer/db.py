import os
from psycopg2 import connect, extras
from dotenv import load_dotenv
from datetime import date

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


def connect_db():
    return connect(DATABASE_URL)


def get_data_by_name(url):
    conn = connect_db()
    with conn.cursor(cursor_factory=extras.NamedTupleCursor) as curs:
        curs.execute('SELECT * FROM urls WHERE name=%s', (url,))
        existing = curs.fetchone()
    conn.close()
    return existing


def get_data_by_id(id):
    conn = connect_db()
    with conn.cursor(cursor_factory=extras.NamedTupleCursor) as curs:
        curs.execute('SELECT * FROM urls WHERE id=%s', (id,))
        existing = curs.fetchone()
    conn.close()
    return existing


def get_all_urls():
    conn = connect_db()
    with conn.cursor(cursor_factory=extras.NamedTupleCursor) as curs:
        curs.execute('SELECT * FROM urls')
        urls = curs.fetchall()
    conn.close()
    return urls


def add_url(url):
    conn = connect_db()
    with conn.cursor(cursor_factory=extras.NamedTupleCursor) as curs:
        curs.execute(
            'INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id',
            (url, date.today())
        )
        id = curs.fetchone().id
    conn.commit()
    conn.close()
    return id
