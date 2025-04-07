#!/usr/bin/env python3
import os
import sys
import argparse
import datetime
from urllib.parse import urlparse, parse_qs

# Import modules
from components.video_downloader import download_video
from components.transcript_downloader import (
    download_transcript, fetch_video_metadata, save_transcript
)

def parse_args():
    parser = argparse.ArgumentParser(description="Download YouTube videos & transcripts.")
    parser.add_argument("-u", "--url", help="Single YouTube URL")
    parser.add_argument("-f", "--file", help="File containing YouTube URLs, one per line")
    return parser.parse_args()

def get_video_id(youtube_url):
    """
    Extract the 'v=' parameter from a typical YouTube URL: 
    e.g. https://www.youtube.com/watch?v=abc123 => 'abc123'
    or short link forms. We'll do minimal logic.
    """
    parsed = urlparse(youtube_url)
    if parsed.query:
        qs = parse_qs(parsed.query)
        if 'v' in qs:
            return qs['v'][0]
    # If it's a short youtu.be link or something else, you might parse differently
    # But let's keep it simple for now.
    return None

def main():
    args = parse_args()

    # Decide input sources
    youtube_urls = []
    if args.url:
        youtube_urls.append(args.url)
    elif args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            youtube_urls = [line.strip() for line in f if line.strip()]
    else:
        print("Please provide --url <URL> or --file <file_of_urls>")
        sys.exit(1)

    # Determine output root directory from env or default
    output_root = os.environ.get("YOUTUBE_OUTPUTS_PATH", "")
    if not output_root:
        # default
        output_root = os.path.expanduser("~/youtube-downloads")

    # Create date subfolder
    date_str = datetime.date.today().strftime("%Y%m%d")
    date_subdir = os.path.join(output_root, date_str)
    os.makedirs(date_subdir, exist_ok=True)

    for url in youtube_urls:
        print(f"\n[INFO] Processing URL: {url}")

        # 1) Download the video to date_subdir
        video_path = download_video(url, date_subdir)
        if video_path:
            print(f"[+] Video saved: {video_path}")
        else:
            print("[-] Video download failed or not found.")
        
        # 2) Download transcript
        video_id = get_video_id(url)
        if not video_id:
            print("[-] Could not parse video ID from URL. Skipping transcript.")
            continue

        transcript = download_transcript(video_id)
        if transcript:
            metadata = fetch_video_metadata(video_id)
            # save the transcript in the same date_subdir
            save_transcript(transcript, metadata, date_subdir)
        else:
            print("[-] No transcript available or error occurred.")

    print("\n[Done] All tasks complete.")

if __name__ == "__main__":
    main()

"""
╰─$ python3 app/main.py --url https://www.youtube.com/watch\?v\=Qm7k1CPFkIc                                                                                          1 ↵

[INFO] Processing URL: https://www.youtube.com/watch?v=Qm7k1CPFkIc
[+] Video saved: /Users/tasteless/youtube-downloads/20250407/How-to-Get-Someone's-Password.mp4
Transcript saved to: /Users/tasteless/youtube-downloads/20250407/How_to_Get_Someone's_Password-Jack_Rhysider.txt

[Done] All tasks complete.
"""