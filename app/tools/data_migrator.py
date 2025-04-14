#!/usr/bin/env python3
"""
youtube_data_migrator.py

Moves video and transcript files from dated folders (e.g. 20250408) in ~/youtube-downloads/
to an external drive at /Volumes/2025-J4F-01/scraped_data/youtube-downloads/
Uses rsync to prevent corruption and logs migration details for each file in SQLite.
Also syncs (not deletes) metadata.sqlite.
"""

import os
import sys
import subprocess
import sqlite3
from datetime import datetime
from pathlib import Path

SOURCE_DIR = Path.home() / "youtube-downloads"
DEST_DIR = Path("/Volumes/2025-J4F-01/scraped_data/youtube-downloads")
TRACKER_DB = SOURCE_DIR / "migration_tracker.sqlite"

def init_db():
    os.makedirs(SOURCE_DIR, exist_ok=True)
    conn = sqlite3.connect(TRACKER_DB)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS migration_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_path TEXT,
        moved_path TEXT,
        filename TEXT,
        file_size INTEGER,
        file_type TEXT,
        date_migrated TEXT
    )""")
    conn.commit()
    return conn

def file_already_migrated(original_path, conn):
    c = conn.cursor()
    c.execute("SELECT 1 FROM migration_log WHERE original_path = ?", (str(original_path),))
    return c.fetchone() is not None

def log_file_migration(original_path, moved_path, filename, file_size, file_type, conn):
    c = conn.cursor()
    c.execute("""
        INSERT INTO migration_log (original_path, moved_path, filename, file_size, file_type, date_migrated)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        str(original_path), str(moved_path), filename, file_size, file_type,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()

def rsync_file(src, dst_dir, dry_run=False):
    dst = dst_dir / src.name
    cmd = ["rsync", "-avh", "--remove-source-files", str(src), str(dst)]
    if dry_run:
        cmd.insert(2, "--dry-run")
    subprocess.run(cmd, check=True)
    return dst

def migrate_folders(dry_run=False):
    conn = init_db()
    os.makedirs(DEST_DIR, exist_ok=True)

    for folder in sorted(SOURCE_DIR.iterdir()):
        if not folder.is_dir() or not folder.name.isdigit():
            continue

        for file_path in folder.iterdir():
            if file_path.suffix not in ['.mp4', '.txt']:
                continue

            if file_path.name.endswith(".part"):
                print(f"[SKIP] Incomplete file (still downloading): {file_path.name}")
                continue

            if file_already_migrated(file_path, conn):
                print(f"[SKIP] Already migrated: {file_path.name}")
                continue

            print(f"[INFO] Migrating: {file_path.name}")
            try:
                file_size = file_path.stat().st_size
                file_type = "video" if file_path.suffix == ".mp4" else "transcript"

                dest_path = rsync_file(file_path, DEST_DIR, dry_run=dry_run)

                if not dry_run:
                    log_file_migration(file_path, dest_path, file_path.name, file_size, file_type, conn)
            except subprocess.CalledProcessError as e:
                print(f"[ERROR] Failed to migrate {file_path.name}: {e}")

    conn.close()

def sync_metadata_sqlite():
    src = SOURCE_DIR / "metadata.sqlite"
    dst = DEST_DIR / "metadata.sqlite"
    if not src.exists():
        print("[WARN] metadata.sqlite not found, skipping copy.")
        return

    print("[SYNC] Copying metadata.sqlite to HDD (overwrite allowed).")
    subprocess.run(["rsync", "-avh", str(src), str(dst)], check=True)

def main():
    dry_run = "--dry-run" in sys.argv
    print("[START] YouTube data migration")
    migrate_folders(dry_run=dry_run)
    if not dry_run:
        sync_metadata_sqlite()
    print("[DONE] Migration process completed.")

if __name__ == "__main__":
    main()
