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
