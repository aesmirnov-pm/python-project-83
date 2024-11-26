import datetime as dt
import contextlib
from functools import partial

import psycopg2
from psycopg2.extras import NamedTupleCursor


SELECT_URL = 'SELECT * FROM urls'

INSERT_URL = """
INSERT INTO urls (name, created_at)
VALUES (%s, %s)
RETURNING id;
"""


@contextlib.contextmanager
def connection(db_url):
    conn = psycopg2.connect(db_url)
    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    else:
        conn.commit()
    finally:
        conn.close()


def get_url_by(conn, value, field):
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(SELECT_URL.format(column=field), (value, ))
        found_item = curs.fetchone()
    return found_item


get_url_by_name = partial(get_url_by, field='name')
get_url_by_id = partial(get_url_by, field='id')


def get_urls(conn):
    with conn.cursor() as curs:
        curs.execute(SELECT_URL)
        all_entries = curs.fetchall()
    return all_entries


def add_to_urls(conn, url):
    with conn.cursor() as curs:
        curs.execute(INSERT_URL, (url, dt.datetime.now()))
        returned_id, = curs.fetchone()
    return returned_id
