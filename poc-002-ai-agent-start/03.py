# File: agent_runner.py
from summarizer import summarize_content
from strategist import generate_strategy
from scraper import scrape_youtube_transcript
from storage import store_result


def run_pipeline(youtube_url: str):
    print("[+] Scraping YouTube content...")
    content = scrape_youtube_transcript(youtube_url)

    print("[+] Summarizing content...")
    summary = summarize_content(content)

    print("[+] Generating strategy...")
    strategy = generate_strategy(summary)

    store_result(youtube_url, content, summary, strategy)

    print("[✓] DONE. Here's the final output:")
    print("\n--- SUMMARY ---\n", summary)
    print("\n--- STRATEGY ---\n", strategy)


if __name__ == "__main__":
    # Example URL; replace with a real one or connect to input source
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    run_pipeline(test_url)


# File: scraper.py
import yt_dlp
import re

def scrape_youtube_transcript(url):
    print(f"[+] Downloading transcript from {url}...")
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
        'outtmpl': '%(id)s.%(ext)s',
    }
    video_id = None

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        video_id = info['id']
        subtitles = info.get('automatic_captions', {}).get('en')
        if not subtitles:
            return "No transcript available."

        transcript_url = subtitles[0]['url']
        import requests
        r = requests.get(transcript_url)
        transcript = re.sub('<[^<]+?>', '', r.text)
        return transcript


# File: summarizer.py
import requests
import os

def summarize_content(content):
    print("[+] Calling Ollama for summary...")
    model = os.getenv("OLLAMA_MODEL", "llama3:70b")
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": model,
        "prompt": f"Summarize the following:\n\n{content}\n",
        "stream": False
    })
    return response.json()["response"]


# File: strategist.py
import requests
import os

def generate_strategy(summary):
    print("[+] Calling Ollama for strategic insight...")
    model = os.getenv("OLLAMA_MODEL", "llama3:70b")
    prompt = f"Given the summary below, generate actionable strategies or insights:\n\n{summary}"

    response = requests.post("http://localhost:11434/api/generate", json={
        "model": model,
        "prompt": prompt,
        "stream": False
    })
    return response.json()["response"]


# File: storage.py
import sqlite3
import os
from datetime import datetime

def store_result(source_url, transcript, summary, strategy):
    db_path = os.getenv("SQLITE_DB_PATH", "./ai_agent.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS ai_outputs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_url TEXT NOT NULL,
            transcript TEXT,
            summary TEXT,
            strategy TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        INSERT INTO ai_outputs (source_url, transcript, summary, strategy, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (source_url, transcript, summary, strategy, datetime.utcnow().isoformat()))

    conn.commit()
    cur.close()
    conn.close()


# File: .env
# Configuration for Ollama model
OLLAMA_MODEL=llama3:70b

# SQLite database file path
SQLITE_DB_PATH=./ai_agent.db


# File: db_schema.sql
-- For long-term storage of transcripts, summaries, and strategies (SQLite format)
CREATE TABLE IF NOT EXISTS ai_outputs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_url TEXT NOT NULL,
    transcript TEXT,
    summary TEXT,
    strategy TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
