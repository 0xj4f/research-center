#!/usr/bin/env python3
import os
import sys
import argparse
import datetime
import re
from urllib.parse import urlparse, parse_qs

from components.video_downloader import download_video
from components.transcript_downloader import (
    fetch_video_metadata, download_transcript, save_transcript
)
# from components.store_metadata import init_db, insert_metadata
from components.sqlite_interface import init_db, insert_metadata, youtube_url_exists

def parse_args():
    parser = argparse.ArgumentParser(description="Download YouTube videos & transcripts with consistent naming, store metadata.")
    parser.add_argument("-u", "--url", help="Single YouTube URL")
    parser.add_argument("-f", "--file", help="File containing YouTube URLs, one per line")
    return parser.parse_args()

def get_video_id(youtube_url):
    parsed = urlparse(youtube_url)
    qs = parse_qs(parsed.query)
    if 'v' in qs:
        return qs['v'][0]
    if 'youtu.be' in parsed.netloc:
        return parsed.path.strip('/')
    return None

def sanitize_string(s):
    s = s.replace("'", "")
    s = re.sub(r'[^a-zA-Z0-9]+', '_', s)
    return s.strip('_')

def main():
    args = parse_args()

    # Build list of URLs
    youtube_urls = []
    if args.url:
        youtube_urls.append(args.url)
    elif args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            youtube_urls = [line.strip() for line in f if line.strip()]
    else:
        print("Please provide --url <URL> or --file <FILE>")
        sys.exit(1)

    # Start or open the DB
    conn = init_db()

    # Output root from env or default
    root = os.environ.get("YOUTUBE_OUTPUTS_PATH", "")
    if not root:
        root = os.path.expanduser("~/youtube-downloads")

    today_str = datetime.date.today().strftime("%Y%m%d")
    date_dir = os.path.join(root, today_str)
    os.makedirs(date_dir, exist_ok=True)

    for url in youtube_urls:
        print(f"\n[INFO] Processing: {url}")

        vid_id = get_video_id(url)
        if not vid_id:
            print(f"[ERROR] Could not parse video ID from {url}. Skipping.")
            continue

        if youtube_url_exists(url):
            print(f"[SKIP] URL already exists in DB: {url}")
            continue


        meta = fetch_video_metadata(vid_id)
        raw_title = meta['title']
        raw_author = meta['author']

        title = sanitize_string(raw_title)
        author = sanitize_string(raw_author)
        base_name = f"{title}-{author}"

        # Download transcript
        transcript = download_transcript(vid_id)
        transcript_path = None
        if transcript:
            transcript_path = os.path.join(date_dir, f"{base_name}.txt")
            save_transcript(transcript, date_dir, base_name)
        else:
            print("[!] No transcript for this video or disabled.")

        # Download video
        video_path = download_video(url, date_dir, final_filename_base=base_name)
        if video_path:
            print(f"[+] Video downloaded: {video_path}")
        else:
            print("[!] Video not saved properly or error.")
            video_path = None

        # Insert into DB
        date_downloaded = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row_id = insert_metadata(
            conn,
            youtube_url=url,
            video_title=raw_title,
            author=raw_author,
            video_path=video_path if video_path else "",
            transcript_path=transcript_path if transcript_path else "",
            date_downloaded=date_downloaded
        )
        print(f"[DB] Inserted row id={row_id}")

    conn.close()
    print("\n[DONE] All tasks completed.")

if __name__ == "__main__":
    main()
