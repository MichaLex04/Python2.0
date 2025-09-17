# py/db_connection.py
import psycopg2
from psycopg2.extras import RealDictCursor
import os

def get_connection():
    conn = psycopg2.connect(
        dbname=os.getenv("PG_DB", "racionador"),
        user=os.getenv("PG_USER", "postgres"),
        password=os.getenv("PG_PASS", "password"),
        host=os.getenv("PG_HOST", "localhost"),
        port=os.getenv("PG_PORT", "5432")
    )
    return conn

def query_fetchall(query, params=None):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            return cur.fetchall()
    finally:
        conn.close()

def query_fetchone(query, params=None):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            return cur.fetchone()
    finally:
        conn.close()

def query_execute(query, params=None, commit=True):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            if commit:
                conn.commit()
    finally:
        conn.close()