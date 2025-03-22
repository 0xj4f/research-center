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
import psycopg2
import os

def store_result(source_url, transcript, summary, strategy):
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME", "ai_agent"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "password"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432")
    )
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO ai_outputs (source_url, transcript, summary, strategy)
        VALUES (%s, %s, %s, %s)
    """, (source_url, transcript, summary, strategy))
    conn.commit()
    cur.close()
    conn.close()


# File: .env
# Configuration for Ollama model
OLLAMA_MODEL=llama3:70b

# PostgreSQL database configuration
DB_NAME=ai_agent
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432


# File: db_schema.sql
-- For long-term storage of transcripts, summaries, and strategies
CREATE TABLE IF NOT EXISTS ai_outputs (
    id SERIAL PRIMARY KEY,
    source_url TEXT NOT NULL,
    transcript TEXT,
    summary TEXT,
    strategy TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
