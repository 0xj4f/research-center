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

def parse_args():
    parser = argparse.ArgumentParser(description="Download YouTube videos & transcripts with consistent naming.")
    parser.add_argument("-u", "--url", help="Single YouTube URL")
    parser.add_argument("-f", "--file", help="File containing YouTube URLs, one per line")
    return parser.parse_args()

def get_video_id(youtube_url):
    """
    Extract the 'v=' parameter from standard YouTube links,
    or handle short youtu.be link. Return None if not found.
    """
    parsed = urlparse(youtube_url)
    qs = parse_qs(parsed.query)
    if 'v' in qs:
        return qs['v'][0]
    # handle short youtu.be/<id>
    if 'youtu.be' in parsed.netloc:
        # path might be the ID
        return parsed.path.strip('/')
    return None

def sanitize_string(s):
    """
    Replace spaces, apostrophes, or other non-alphanumeric with underscore.
    """
    # remove apostrophe in a naive approach or replace with _
    # then replace leftover non-alphanumerics with _
    s = s.replace("'", "")  # remove apostrophes
    s = re.sub(r'[^a-zA-Z0-9]+', '_', s)
    return s.strip('_')

def main():
    args = parse_args()

    # Gather list of URLs
    youtube_urls = []
    if args.url:
        youtube_urls.append(args.url)
    elif args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            youtube_urls = [line.strip() for line in f if line.strip()]
    else:
        print("Please provide --url <URL> or --file <FILE>")
        sys.exit(1)

    # Use env or default
    root = os.environ.get("YOUTUBE_OUTPUTS_PATH", "")
    if not root:
        root = os.path.expanduser("~/youtube-downloads")

    # date subfolder
    today_str = datetime.date.today().strftime("%Y%m%d")
    date_dir = os.path.join(root, today_str)
    os.makedirs(date_dir, exist_ok=True)

    for url in youtube_urls:
        print(f"\n[INFO] Processing: {url}")
        vid_id = get_video_id(url)
        if not vid_id:
            print(f"[ERROR] Could not parse video ID from {url}. Skipping.")
            continue

        # 1) fetch metadata
        meta = fetch_video_metadata(vid_id)  # {title, author}
        title = sanitize_string(meta['title'])
        author = sanitize_string(meta['author'])
        base_name = f"{title}-{author}"  # e.g. "How_to_Get_Someones_Password-Jack_Rhysider"

        # 2) Download transcript
        transcript = download_transcript(vid_id)
        if transcript:
            save_transcript(transcript, date_dir, base_name)
        else:
            print("[!] No transcript or disabled for this video.")

        # 3) Download video using the same base_name => => base_name.mp4
        video_path = download_video(url, date_dir, final_filename_base=base_name)
        if video_path:
            print(f"[+] Video downloaded: {video_path}")
        else:
            print("[!] Video download failed or was not saved properly.")

    print("\n[DONE] All tasks completed.")

if __name__ == "__main__":
    main()
"""
╰─$ python3 app/main.py --url https://www.youtube.com/watch\?v\=Qm7k1CPFkIc

[INFO] Processing: https://www.youtube.com/watch?v=Qm7k1CPFkIc
[+] Transcript saved to /Users/tasteless/youtube-downloads/20250407/How_to_Get_Someones_Password-Jack_Rhysider.txt
[+] Video downloaded: /Users/tasteless/youtube-downloads/20250407/How_to_Get_Someones_Password-Jack_Rhysider.mp4

[DONE] All tasks completed
"""
