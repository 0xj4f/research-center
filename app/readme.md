
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
ID    YOUTUBE_URL                    TITLE                          VIDEO_PATH                     TRANSCRIPT_PATH                DATE_DOWN            LLM1
------------------------------------------------------------------------------------------------------------------------------------------------------
1     https://www.youtube.com/watc.. How_to_Get_Someones_Password.. /Users/tasteless/youtube-dow.. /Users/tasteless/youtube-dow.. 2025-04-07 15:00:36  N

[DONE]
```

