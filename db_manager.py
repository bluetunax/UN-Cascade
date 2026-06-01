# /db_manager.py

import sqlite3
import json
from datetime import datetime

DB_FILE = "sessions.db"

def init_db():
    """Initializes the SQLite database and creates the sessions table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            country TEXT NOT NULL,
            year TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            macro_data TEXT NOT NULL,
            micro_data TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_snapshot(country, year, macro_data, micro_data):
    """Saves the processed API data into the local SQLite database as a JSON string."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    macro_json = json.dumps(macro_data)
    micro_json = json.dumps(micro_data)
    
    cursor.execute('''
        INSERT INTO snapshots (country, year, timestamp, macro_data, micro_data)
        VALUES (?, ?, ?, ?, ?)
    ''', (country, year, timestamp, macro_json, micro_json))
    
    # Get the ID of the newly created snapshot so we can use it in the URL
    session_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    return session_id

def get_snapshot(session_id):
    """Retrieves a specific snapshot by its ID and un-JSONs the data."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT country, year, timestamp, macro_data, micro_data FROM snapshots WHERE id = ?', (session_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "country": row[0],
            "year": row[1],
            "timestamp": row[2],
            "macro_data": json.loads(row[3]),
            "micro_data": json.loads(row[4]),
            "is_offline": True
        }
    return None

def get_all_sessions():
    """Retrieves a list of all saved sessions for the homepage history table."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Get basic info, ordered by newest first
    cursor.execute('SELECT id, country, year, timestamp FROM snapshots ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    
    sessions = []
    for row in rows:
        sessions.append({
            "id": row[0],
            "country": row[1],
            "year": row[2],
            "timestamp": row[3]
        })
    return sessions