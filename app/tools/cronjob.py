#!/usr/bin/env python3
import subprocess
import shutil
import os
from datetime import datetime
from pathlib import Path

SOURCE_DIR = Path.home() / "youtube-downloads"
SIZE_LIMIT_GB = 10
MIGRATOR_SCRIPT = Path(__file__).parent / "data_migrator.py"
LOG_FILE = SOURCE_DIR / "cronjob_migration.log"

def get_folder_size_gb(path: Path) -> float:
    """Returns the size of a folder in gigabytes."""
    total = 0
    for root, _, files in os.walk(path):
        for f in files:
            try:
                fp = os.path.join(root, f)
                total += os.path.getsize(fp)
            except FileNotFoundError:
                continue  # file was likely moved during scanning
    return total / (1024 ** 3)


def write_log(log_msg):
    print(log_msg)
    with open(LOG_FILE, "a") as f:
        f.write(log_msg + "\n")

def main():
    current_size = get_folder_size_gb(SOURCE_DIR)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    readable_path = str(SOURCE_DIR)

    if current_size >= SIZE_LIMIT_GB:
        log_msg = f"[{now}] Triggering migration. Folder '{readable_path}' size: {current_size:.2f} GB, Limit Size {SIZE_LIMIT_GB}"
        write_log(log_msg=log_msg)
        subprocess.run(["python3", str(MIGRATOR_SCRIPT)], check=True)

        # Finished log
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current_size = get_folder_size_gb(SOURCE_DIR)
        log_msg = f"[{now}] Finished Data Migration '{readable_path}' size: {current_size:.2f} GB"
        write_log(log_msg=log_msg)
    else:
        log_msg = f"[{now}] No action. Folder '{readable_path}' size: {current_size:.2f} GB"
        write_log(log_msg=log_msg)

if __name__ == "__main__":
    main()
