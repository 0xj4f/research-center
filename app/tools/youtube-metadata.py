#!/usr/bin/env python3
"""
youtube-metadata.py

Usage:
  python youtube-metadata.py [--all]

If no argument is passed, shows the last 10 entries in descending order by ID.
If --all is passed, shows all entries in the table.
"""

import os
import sys
import argparse
import sqlite3

def get_db_path():
    """
    Return the path for metadata.sqlite, defaulting to ~/youtube-downloads/metadata.sqlite
    """
    home = os.path.expanduser("~")
    default_dir = os.path.join(home, "youtube-downloads")
    os.makedirs(default_dir, exist_ok=True)  # Ensure it exists
    return os.path.join(default_dir, "metadata.sqlite")

def parse_args():
    parser = argparse.ArgumentParser(
        description="Query youtube-downloads/metadata.sqlite for stored entries."
    )
    parser.add_argument("-a", "--all", action="store_true",
                        help="Show all entries (otherwise show last 10).")
    return parser.parse_args()

def main():
    args = parse_args()
    db_path = get_db_path()

    if not os.path.exists(db_path):
        print(f"[ERROR] No metadata DB found at {db_path}")
        sys.exit(1)

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Let's first see how many total rows we have
    c.execute("SELECT COUNT(*) FROM downloads;")
    total_count = c.fetchone()[0]

    print(f"[INFO] Found {total_count} total entries in 'downloads' table.")

    if total_count == 0:
        print("[INFO] No rows to show.")
        conn.close()
        return

    if args.all:
        query = "SELECT id, youtube_url, video_title, video_path, transcript_path, date_downloaded, llm_1_analyze FROM downloads ORDER BY id DESC"
    else:
        query = "SELECT id, youtube_url, video_title, video_path, transcript_path, date_downloaded, llm_1_analyze FROM downloads ORDER BY id DESC LIMIT 10"

    c.execute(query)
    rows = c.fetchall()

    if not rows:
        print("[INFO] No rows returned.")
        conn.close()
        return

    # Print in a quick table format
    print("\n=== Download Entries ===")
    # We'll do a simple spaced format. 
    # For a more advanced approach, you could use texttable or rich.
    print(f"{'ID':<5} {'YOUTUBE_URL':<30} {'TITLE':<30} {'VIDEO_PATH':<30} {'TRANSCRIPT_PATH':<30} {'DATE_DOWN':<20} {'LLM1'}")
    print("-"*150)

    for r in rows:
        (row_id, youtube_url, video_title, video_path, transcript_path, date_downloaded, llm_flag) = r
        # Truncate to avoid line overflow if desired
        y_url = (youtube_url[:28] + "..") if len(youtube_url) > 30 else youtube_url
        v_title = (video_title[:28] + "..") if len(video_title) > 30 else video_title
        vid_path = (video_path[:28] + "..") if len(video_path) > 30 else video_path
        txt_path = (transcript_path[:28] + "..") if len(transcript_path) > 30 else transcript_path
        date_str = date_downloaded if date_downloaded else "-"
        llm_str = "Y" if llm_flag else "N"

        print(f"{row_id:<5} {y_url:<30} {v_title:<30} {vid_path:<30} {txt_path:<30} {date_str:<20} {llm_str}")

    conn.close()
    print("\n[DONE]")

if __name__ == "__main__":
    main()
