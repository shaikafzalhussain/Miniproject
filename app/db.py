import sqlite3
from sqlite3 import Row

CREATE_NOTES_SQL = """
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    content TEXT,
    created_at TEXT
);
"""

def init_db(path='data.db'):
    conn = sqlite3.connect(path)
    conn.execute(CREATE_NOTES_SQL)
    conn.commit()
    conn.close()

def get_db(path='data.db'):
    conn = sqlite3.connect(path)
    conn.row_factory = Row
    return conn

def query_db(path, query, args=(), one=False):
    conn = get_db(path)
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    if one:
        return dict(rv[0]) if rv else None
    return [dict(r) for r in rv]

