# Youtube Scraper App 
> v3.0.0

FEATURES
- Downloads Transcript
- Downloads Videos 
- Store Metadata


## USAGE

single 
```bash
╰─$ python3 app/main.py --url https://www.youtube.com/watch\?v\=Qm7k1CPFkIc

[INFO] Processing: https://www.youtube.com/watch?v=Qm7k1CPFkIc
[+] Transcript saved to /Users/tasteless/youtube-downloads/20250407/How_to_Get_Someones_Password-Jack_Rhysider.txt
[+] Video downloaded: /Users/tasteless/youtube-downloads/20250407/How_to_Get_Someones_Password-Jack_Rhysider.mp4
[DB] Inserted row id=1

[DONE] All tasks completed.

╰─$ python3 app/tools/youtube-metadata.py
[INFO] Found 1 total entries in 'downloads' table.

=== Download Entries ===
ID    YOUTUBE_URL                    TITLE                     AUTHOR               VIDEO_PATH                     TRANSCRIPT_PATH                DATE_DOWN            LLM1
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
1     https://www.youtube.com/watc.. How to Get Someone's Pa.. Jack Rhysider        /Users/tasteless/youtube-dow.. /Users/tasteless/youtube-dow.. 2025-04-07 15:16:34  N

[DONE]
```


File List 
```bash
╰─$ python3 app/main.py                                                    
Please provide --url <URL> or --file <FILE>
(.venv) ╭─tasteless@shadow ~/Repo/00-JAF/research-center ‹main●› 
╰─$ python3 app/main.py --file list.txt                                                                                                                                                                                  1 ↵

[INFO] Processing: https://www.youtube.com/watch?v=JsVtHqICeKE
[+] Transcript saved to /Users/tasteless/youtube-downloads/20250407/DEFCON_19_Steal_Everything_Kill_Everyone_Cause_Total_Financial_Ruin_w_speaker-Christiaan008.txt
[+] Video downloaded: /Users/tasteless/youtube-downloads/20250407/DEFCON_19_Steal_Everything_Kill_Everyone_Cause_Total_Financial_Ruin_w_speaker-Christiaan008.mp4
[DB] Inserted row id=2

[INFO] Processing: https://www.youtube.com/watch?v=H9yQpsreMVI
[+] Transcript saved to /Users/tasteless/youtube-downloads/20250407/DEF_CON_17_Jayson_E_Street_Dispelling_the_Myths_and_Discussing_the_Facts_of_Global_Cyber_Warfare-DEFCONConference.txt
[+] Video downloaded: /Users/tasteless/youtube-downloads/20250407/DEF_CON_17_Jayson_E_Street_Dispelling_the_Myths_and_Discussing_the_Facts_of_Global_Cyber_Warfare-DEFCONConference.mp4
[DB] Inserted row id=3

[DONE] All tasks completed.

╰─$ python3 app/tools/youtube-metadata.py
[INFO] Found 3 total entries in 'downloads' table.

=== Download Entries ===
ID    YOUTUBE_URL                    TITLE                     AUTHOR               VIDEO_PATH                     TRANSCRIPT_PATH                DATE_DOWN            LLM1
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
3     https://www.youtube.com/watc.. DEF CON 17 - Jayson E S.. DEFCONConference     /Users/tasteless/youtube-dow.. /Users/tasteless/youtube-dow.. 2025-04-07 15:37:57  N
2     https://www.youtube.com/watc.. DEFCON 19: Steal Everyt.. Christiaan008        /Users/tasteless/youtube-dow.. /Users/tasteless/youtube-dow.. 2025-04-07 15:37:08  N
1     https://www.youtube.com/watc.. How to Get Someone's Pa.. Jack Rhysider        /Users/tasteless/youtube-dow.. /Users/tasteless/youtube-dow.. 2025-04-07 15:16:34  N

[DONE]
```

Validation if url is already existing
```
╰─$ python3 app/main.py --file list.txt  

[INFO] Processing: https://www.youtube.com/watch?v=JsVtHqICeKE
[SKIP] URL already exists in DB: https://www.youtube.com/watch?v=JsVtHqICeKE

[INFO] Processing: https://www.youtube.com/watch?v=H9yQpsreMVI
[SKIP] URL already exists in DB: https://www.youtube.com/watch?v=H9yQpsreMVI

[INFO] Processing: https://www.youtube.com/watch?v=4qvNRfExoEM
[+] Transcript saved to /Users/tasteless/youtube-downloads/20250408/Symlinks_The_Mortal_Enemy_of_CTF_Creators-Tib3rius.txt
[+] Video downloaded: /Users/tasteless/youtube-downloads/20250408/Symlinks_The_Mortal_Enemy_of_CTF_Creators-Tib3rius.mp4
[DB] Inserted row id=4

[DONE] All tasks completed.
```

## youtube channel crawler
> app/tools/youtube_channel_crawler.py
```
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
```

json structure 
```json 
{
    "channel_name": "JackRhysider",
    "channel_url": "https://www.youtube.com/@JackRhysider/videos",
    "videos": [
        {
            "title": "Secrets of Defcon: Untold Stories From the World's Greatest Hacker Conference \ud83d\udcbe Ep.157: Grifter",
            "url": "https://www.youtube.com/watch?v=RyLlzHvXIDQ",
            "published": "Unknown Date"
        },
        {
            "title": "There's No Way This \"Hitman for Hire\" Website Is Real...Right?\ud83d\udc80Darknet Diaries Ep. 156: Kill List",
            "url": "https://www.youtube.com/watch?v=f2YONut4F6Q",
            "published": "Unknown Date"
        },
    ]
}
```

To save urls as lists
```bash
jq -r '.videos[].url' JackRhysider.json > 01.txt
```


## Data Migration
YouTube Data Migrator
This script safely moves downloaded YouTube videos and transcripts from your Mac to an external hard drive using rsync, with file-level logging into a local SQLite database to prevent duplication and enable audit trails.

Features
- Moves .mp4 and .txt files from ~/youtube-downloads/YYYYMMDD/ to /Volumes/2025-J4F-01/scraped_data/youtube-downloads/
- Preserves metadata by syncing metadata.sqlite (copied, not deleted)
- Prevents data corruption using rsync --remove-source-files
- Tracks every file migrated using migration_tracker.sqlite
- Supports --dry-run mode to preview the migration

|                        Folder                        |                       Purpose                      |
|:----------------------------------------------------:|:--------------------------------------------------:|
| ~/youtube-downloads/YYYYMMDD/                        | Daily scraped videos & transcripts                 |
| ~/youtube-downloads/metadata.sqlite                  | Tracks YouTube metadata                            |
| /Volumes/2025-J4F-01/scraped_data/youtube-downloads/ | Long-term archive                                  |
| ~/youtube-downloads/migration_tracker.sqlite         | Internal migration log                             |


```bash
# safe  preview
python3 data_migrator.py --dry-run

╰─$ python3 app/tools/data_migrator.py
sent 84.77M bytes  received 42 bytes  56.51M bytes/sec
total size is 84.76M  speedup is 1.00
[INFO] Migrating: Ep_4_Panic_at_the_TalkTalk_Board_Room-Jack_Rhysider.txt
building file list ... done
Ep_4_Panic_at_the_TalkTalk_Board_Room-Jack_Rhysider.txt

sent 41.45K bytes  received 42 bytes  82.99K bytes/sec
total size is 41.27K  speedup is 0.99
[INFO] Migrating: When_She_Cant_Hack_the_Lock_She_Hacks_the_Security_Guard_Darknet_Diaries_Ep_90_Jenny-Jack_Rhysider.mp4
building file list ... done
When_She_Cant_Hack_the_Lock_She_Hacks_the_Security_Guard_Darknet_Diaries_Ep_90_Jenny-Jack_Rhysider.mp4

sent 112.10M bytes  received 42 bytes  44.84M bytes/sec
total size is 112.09M  speedup is 1.00
[INFO] Migrating: XBee_Basics_Lesson_3_API_Mode_Digital_Input_from_Remote_Sensor-Jack_Rhysider.txt
building file list ... done
XBee_Basics_Lesson_3_API_Mode_Digital_Input_from_Remote_Sensor-Jack_Rhysider.txt

sent 10.24K bytes  received 42 bytes  20.56K bytes/sec
total size is 10.04K  speedup is 0.98
[INFO] Migrating: A_Clipboard_is_All_You_Need_to_Break_Into_a_Building_Darknet_Diaries_Ep_22_Mini_Stories_Vol_1-Jack_Rhysider.mp4
building file list ... done
A_Clipboard_is_All_You_Need_to_Break_Into_a_Building_Darknet_Diaries_Ep_22_Mini_Stories_Vol_1-Jack_Rhysider.mp4

sent 64.62M bytes  received 42 bytes  129.25M bytes/sec
total size is 64.61M  speedup is 1.00
[INFO] Migrating: Why_Governments_Love_to_Buy_the_Bugs_in_Your_Favorite_Apps_Darknet_Diaries_Ep_98_Zero_Day_Brokers-Jack_Rhysider.mp4
building file list ... done
Why_Governments_Love_to_Buy_the_Bugs_in_Your_Favorite_Apps_Darknet_Diaries_Ep_98_Zero_Day_Brokers-Jack_Rhysider.mp4

sent 138.60M bytes  received 42 bytes  55.44M bytes/sec
total size is 138.58M  speedup is 1.00
[SYNC] Copying metadata.sqlite to HDD (overwrite allowed).
building file list ... done
metadata.sqlite

sent 77.97K bytes  received 42 bytes  156.02K bytes/sec
total size is 77.82K  speedup is 1.00
[DONE] Migration process completed.
```


## TO DO NEXT 

IMPORTANT 
- Check file size of ~/youtube-downloads
```
╰─$ du -sh *
252M    20250407
 12K    metadata.sqlite
```

then we need to a function or component called safety_rails
- function that checks the limit of youtube downloads, the default size of acceptable file limit is 40GB.
- if it we're to exceed we need to exit the program, this should be a guard rail. append as the first step of the url loops. so we can check if we can download the next file.
    - then exit the program and create an error message and file to note where we stop, so we can continue after manual intervention
- next a validator logic that will check if the youtube url is already there, if found there add warning message then skip to the next item.
