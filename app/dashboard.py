#!/usr/bin/env python3
import sqlite3
import shutil
from pathlib import Path
from datetime import datetime, timedelta

DB_PATH = Path.home() / "youtube-downloads/metadata.sqlite"
TRACKER_DB = Path.home() / "youtube-downloads/migration_tracker.sqlite"
DOWNLOADS_DIR = Path.home() / "youtube-downloads"
EXTERNAL_HDD = Path("/Volumes/2025-J4F-01")

def print_header(title):
    print(f"\n{'='*5} {title} {'='*5}")

# Existing SQLite stats enhanced
def sqlite_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM downloads")
    total_entries = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM downloads WHERE video_path != ''")
    total_videos = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM downloads WHERE transcript_path != ''")
    total_transcripts = c.fetchone()[0]

    c.execute("SELECT COUNT(DISTINCT author) FROM downloads")
    unique_channels = c.fetchone()[0]

    today_date = datetime.now().strftime("%Y-%m-%d")
    c.execute("SELECT COUNT(*) FROM downloads WHERE date_downloaded LIKE ?", (f"{today_date}%",))
    today_total = c.fetchone()[0]

    c.execute("""
        SELECT COUNT(*) FROM downloads
        WHERE video_path != '' AND transcript_path != '' AND date_downloaded LIKE ?
    """, (f"{today_date}%",))
    today_success = c.fetchone()[0]

    today_failed = today_total - today_success

    conn.close()

    print_header("SQLite Stats")
    print(f"Total entries scraped:        {total_entries}")
    print(f"Total videos downloaded:      {total_videos}")
    print(f"Total transcripts downloaded: {total_transcripts}")
    print(f"Unique channels:              {unique_channels}")

    print_header("Today's Metrics")
    print(f"Videos scraped today:         {today_total}")
    print(f"Successful downloads today:   {today_success}")
    print(f"Failed downloads today:       {today_failed}")

# Migration stats (Enhanced)
def migration_stats():
    if not TRACKER_DB.exists():
        print("\n[WARN] Migration tracker DB not found.")
        return

    conn = sqlite3.connect(TRACKER_DB)
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM migration_log")
    total_migrated = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM migration_log WHERE file_type = 'video'")
    total_videos_migrated = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM migration_log WHERE file_type = 'transcript'")
    total_transcripts_migrated = c.fetchone()[0]

    week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
    c.execute("SELECT COUNT(*) FROM migration_log WHERE date_migrated >= ?", (week_ago,))
    week_migrated = c.fetchone()[0]

    c.execute("SELECT MAX(date_migrated) FROM migration_log")
    last_migration = c.fetchone()[0] or "Never"

    conn.close()

    print_header("Migration Stats")
    print(f"Total files migrated:         {total_migrated}")
    print(f"Total videos migrated:        {total_videos_migrated}")
    print(f"Total transcripts migrated:   {total_transcripts_migrated}")
    print(f"Files migrated this week:     {week_migrated}")
    print(f"Last migration date:          {last_migration}")

# Disk usage (unchanged)
def disk_usage_stats():
    def get_size_gb(path):
        total, used, free = shutil.disk_usage(path)
        return total / (1024**3), used / (1024**3), free / (1024**3)

    mac_total, mac_used, mac_free = get_size_gb(DOWNLOADS_DIR)
    hdd_total, hdd_used, hdd_free = get_size_gb(EXTERNAL_HDD)

    print_header("Disk Usage (Mac Mini)")
    print(f"Total space:                  {mac_total:.2f} GB")
    print(f"Used space:                   {mac_used:.2f} GB")
    print(f"Free space:                   {mac_free:.2f} GB")

    print_header("External HDD Usage")
    print(f"Total space:                  {hdd_total:.2f} GB")
    print(f"Used space:                   {hdd_used:.2f} GB")
    print(f"Free space:                   {hdd_free:.2f} GB")

# Common errors (unchanged but crucial)
def common_errors():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    today_date = datetime.now().strftime("%Y-%m-%d")
    c.execute("""
        SELECT youtube_url FROM downloads
        WHERE (video_path = '' OR transcript_path = '')
        AND date_downloaded LIKE ?
    """, (f"{today_date}%",))
    errors_today = c.fetchall()
    conn.close()

    error_types = {"403 Forbidden": 0, "Members-only": 0, "Others": 0}
    for (url,) in errors_today:
        if "403" in url:
            error_types["403 Forbidden"] += 1
        elif "members" in url.lower():
            error_types["Members-only"] += 1
        else:
            error_types["Others"] += 1

    print_header("Today's Common Errors")
    for error, count in error_types.items():
        print(f"{error:<20}: {count}")

def main():
    print("\n🟢 [YOUTUBE SCRAPER & MIGRATION DASHBOARD] 🟢")
    sqlite_stats()
    migration_stats()
    disk_usage_stats()
    common_errors()
    print("\n[DONE] ✅")

if __name__ == "__main__":
    main()
