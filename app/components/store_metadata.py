# components/store_metadata.py

import os
import sqlite3

def get_db_path():
    """
    Return the path for metadata.sqlite, defaulting to ~/youtube-downloads/metadata.sqlite.
    """
    root = os.environ.get("YOUTUBE_OUTPUTS_PATH", "")
    if not root:
        home = os.path.expanduser("~")
        root = os.path.join(home, "youtube-downloads")
    # Ensure the directory exists
    os.makedirs(root, exist_ok=True)
    return os.path.join(root, "metadata.sqlite")

def init_db():
    """
    Ensure the database and 'downloads' table exist. Returns a sqlite3.Connection.
    """
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS downloads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        youtube_url TEXT NOT NULL,
        video_title TEXT,
        video_path TEXT,
        transcript_path TEXT,
        date_downloaded TEXT,
        llm_1_analyze BOOLEAN DEFAULT 0
    )
    """)
    conn.commit()
    return conn

def insert_metadata(conn, youtube_url, video_title, video_path, transcript_path, date_downloaded):
    """
    Insert a new row into downloads table.
    Return the row id.
    """
    c = conn.cursor()
    c.execute("""
    INSERT INTO downloads (youtube_url, video_title, video_path, transcript_path, date_downloaded)
    VALUES (?, ?, ?, ?, ?)
    """, (youtube_url, video_title, video_path, transcript_path, date_downloaded))
    conn.commit()
    return c.lastrowid

# add or modify columns as needed (like “author”, “upload_date”, or “notes”)