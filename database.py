import sqlite3
import pandas as pd

DB_NAME = "weather.db"


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        temperature REAL,
        humidity REAL,
        pressure REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def insert_data(temp, hum, press):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO weather
    (temperature, humidity, pressure)
    VALUES (?, ?, ?)
    """, (temp, hum, press))

    conn.commit()
    conn.close()


def fetch_data():
    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql_query(
        "SELECT * FROM weather ORDER BY id DESC",
        conn
    )

    conn.close()
    return df


def clear_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM weather")

    conn.commit()
    conn.close()