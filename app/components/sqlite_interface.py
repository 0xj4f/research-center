# import os
# import sqlite3
# from datetime import datetime


# def get_db_path():
#     """
#     Return the path for metadata.sqlite, defaulting to ~/youtube-downloads/metadata.sqlite
#     """
#     home = os.path.expanduser("~")
#     return os.path.join(home, "youtube-downloads", "metadata.sqlite")


# def init_db():
#     db_path = get_db_path()
#     os.makedirs(os.path.dirname(db_path), exist_ok=True)
#     conn = sqlite3.connect(db_path)
#     c = conn.cursor()
#     c.execute('''CREATE TABLE IF NOT EXISTS downloads (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         youtube_url TEXT UNIQUE,
#         video_title TEXT,
#         author TEXT,
#         video_path TEXT,
#         transcript_path TEXT,
#         date_downloaded TEXT,
#         llm_1_analyze BOOLEAN DEFAULT 0
#     )''')
#     conn.commit()
#     conn.close()


# def insert_metadata(youtube_url, title, author, video_path, transcript_path):
#     db_path = get_db_path()
#     conn = sqlite3.connect(db_path)
#     c = conn.cursor()
#     now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     try:
#         c.execute('''INSERT INTO downloads (youtube_url, video_title, author, video_path, transcript_path, date_downloaded)
#                      VALUES (?, ?, ?, ?, ?, ?)''',
#                   (youtube_url, title, author, video_path, transcript_path, now))
#         conn.commit()
#         print(f"[DB] Inserted row id={c.lastrowid}")
#     except sqlite3.IntegrityError:
#         print("[DB] Skipped: already exists.")
#     conn.close()


def youtube_url_exists(youtube_url):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT 1 FROM downloads WHERE youtube_url = ?", (youtube_url,))
    exists = c.fetchone() is not None
    conn.close()
    return exists


# Optional utility for external usage
def youtube_url_validation(url):
    if youtube_url_exists(url):
        print(f"[SKIP] URL already exists in DB: {url}")
        return False
    return True


# # Initialize on module load
# init_db()

# components/sqlite_interface.py

import os
import sqlite3


def get_db_path():
    """
    Return the path for metadata.sqlite, defaulting to ~/youtube-downloads/metadata.sqlite
    """
    home = os.path.expanduser("~")
    root = os.path.join(home, "youtube-downloads")
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
        author TEXT,
        video_path TEXT,
        transcript_path TEXT,
        date_downloaded TEXT,
        llm_1_analyze BOOLEAN DEFAULT 0
    )
    """)
    conn.commit()
    return conn


def insert_metadata(conn, youtube_url, video_title, author, video_path, transcript_path, date_downloaded):
    """
    Insert a new row into downloads table. Return the row id.
    """
    try:
        c = conn.cursor()
        c.execute("""
        INSERT INTO downloads 
        (youtube_url, video_title, author, video_path, transcript_path, date_downloaded)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (youtube_url, video_title, author, video_path, transcript_path, date_downloaded))
        conn.commit()
        return c.lastrowid
    except sqlite3.Error as e:
        print(f"[DB ERROR] Failed to insert metadata: {e}")
        return None


def youtube_url_exists(conn, youtube_url):
    """
    Check if a YouTube URL already exists in the downloads table. Returns True or False.
    """
    c = conn.cursor()
    c.execute("SELECT id FROM downloads WHERE youtube_url = ?", (youtube_url,))
    return c.fetchone() is not None

def youtube_url_exists(youtube_url):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT 1 FROM downloads WHERE youtube_url = ?", (youtube_url,))
    exists = c.fetchone() is not None
    conn.close()
    return exists


# Optional utility for external usage
def youtube_url_validation(url):
    if youtube_url_exists(url):
        print(f"[SKIP] URL already exists in DB: {url}")
        return False
    return True
