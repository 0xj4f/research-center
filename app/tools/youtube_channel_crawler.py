#!/usr/bin/env python3
"""
youtube_channel_crawler.py

Reads a list of YouTube channel URLs from youtube-channels.txt,
fetches their video metadata using yt-dlp, and saves per-channel
JSON files with basic video information (title, URL, published date).
"""

import os
import subprocess
import json
from urllib.parse import urlparse

# Properly expand ~ to home directory
OUTPUT_DIR = os.path.expanduser("~/youtube-downloads/watchlist/")
CHANNEL_LIST_FILE = "youtube-channels.txt"
MAX_VIDEOS = 1000  # Adjust if needed


def sanitize_channel_name(url):
    """
    Extract a clean name from a YouTube channel URL.
    E.g., https://www.youtube.com/@JackRhysider/videos → JackRhysider
    """
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    # Remove trailing '/videos' or any extra subpaths
    if path.endswith("/videos"):
        path = path[:-7]
    if path.startswith("@"):
        path = path[1:]
    return path.replace("/", "_")  # Just in case of other nested paths


def get_videos_for_channel(channel_url):
    """
    Uses yt-dlp to fetch metadata for the channel videos.
    Returns a list of videos with title, url, and upload_date.
    """
    try:
        result = subprocess.run(
            [
                "yt-dlp",
                "--flat-playlist",
                "--dump-json",
                "--playlist-end",
                str(MAX_VIDEOS),
                channel_url,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            check=True
        )
        lines = result.stdout.strip().split("\n")
        videos = []
        for line in lines:
            data = json.loads(line)
            video_id = data.get("id")
            title = data.get("title", "Unknown Title")
            upload_date = data.get("upload_date", "Unknown Date")
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            videos.append({
                "title": title,
                "url": video_url,
                "published": upload_date
            })
        return videos
    except subprocess.CalledProcessError:
        print(f"[ERROR] Failed to fetch videos for {channel_url}")
        return []


def save_channel_json(channel_name, channel_url, videos):
    """
    Saves the collected videos into a per-channel JSON file.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    data = {
        "channel_name": channel_name,
        "channel_url": channel_url,
        "videos": videos
    }
    filename = os.path.join(OUTPUT_DIR, f"{channel_name}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"[+] Saved {len(videos)} videos to {filename}")


def main():
    if not os.path.exists(CHANNEL_LIST_FILE):
        print(f"[ERROR] {CHANNEL_LIST_FILE} not found.")
        return

    with open(CHANNEL_LIST_FILE, "r") as f:
        channels = [line.strip() for line in f if line.strip()]

    for channel_url in channels:
        print(f"[INFO] Crawling: {channel_url}")
        channel_name = sanitize_channel_name(channel_url)
        videos = get_videos_for_channel(channel_url)
        save_channel_json(channel_name, channel_url, videos)

    print("\n[✓] All channels processed.")


if __name__ == "__main__":
    main()



"""
╰─$ python3 app/tools/youtube_channel_crawler.py                                                                                                                                                                         1 ↵
[INFO] Crawling: https://www.youtube.com/@JackRhysider/videos
[+] Saved 183 videos to /Users/tasteless/youtube-downloads/watchlist/JackRhysider.json
[INFO] Crawling: https://www.youtube.com/@DEFCONConference/videos
[+] Saved 1000 videos to /Users/tasteless/youtube-downloads/watchlist/DEFCONConference.json
[INFO] Crawling: https://www.youtube.com/@Tib3rius/videos
[+] Saved 179 videos to /Users/tasteless/youtube-downloads/watchlist/Tib3rius.json
[INFO] Crawling: https://www.youtube.com/@LiveOverflow/videos
[+] Saved 409 videos to /Users/tasteless/youtube-downloads/watchlist/LiveOverflow.json
[INFO] Crawling: https://www.youtube.com/@LowLevelTV/videos
[+] Saved 199 videos to /Users/tasteless/youtube-downloads/watchlist/LowLevelTV.json
[INFO] Crawling: https://www.youtube.com/@NahamSec/videos
[+] Saved 350 videos to /Users/tasteless/youtube-downloads/watchlist/NahamSec.json

[✓] All channels processed.
"""