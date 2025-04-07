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
    

if not