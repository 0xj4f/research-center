# import sys
# from yt_dlp import YoutubeDL

# def download_video(video_url):
#     try:
#         print(f"Downloading: {video_url}")
#         with YoutubeDL({'format': 'best'}) as ydl:
#             ydl.download([video_url])
#         print("Download complete.")
#     except Exception as e:
#         print("Download failed:", str(e))

# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("Usage: python3 yt_downloader.py <youtube_url>")
#         sys.exit(1)

#     download_video(sys.argv[1])

# ╰─$ python3 yt_downloader.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Downloading: https://www.youtube.com/watch?v=dQw4w9WgXcQ
# [youtube] Extracting URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
# [youtube] dQw4w9WgXcQ: Downloading webpage
# [youtube] dQw4w9WgXcQ: Downloading tv client config
# [youtube] dQw4w9WgXcQ: Downloading player 73381ccc-main
# [youtube] dQw4w9WgXcQ: Downloading tv player API JSON
# [youtube] dQw4w9WgXcQ: Downloading ios player API JSON
# [youtube] dQw4w9WgXcQ: Downloading m3u8 information
# [info] dQw4w9WgXcQ: Downloading 1 format(s): 18
# [download] Destination: Rick Astley - Never Gonna Give You Up (Official Music Video) [dQw4w9WgXcQ].mp4
# [download] 100% of    8.68MiB in 00:00:00 at 14.77MiB/s
# Download complete.

"""
VERSION 2
"""

import os
import sys
from yt_dlp import YoutubeDL

def download_video(video_url):
    try:
        output_dir = "./youtube-videos"
        os.makedirs(output_dir, exist_ok=True)

        ydl_opts = {
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'format': 'best',
            'quiet': False,
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)

        # Rename file: replace spaces with dashes
        base_dir, original_filename = os.path.split(filename)
        new_filename = original_filename.replace(" ", "-")
        new_filepath = os.path.join(base_dir, new_filename)

        if original_filename != new_filename:
            os.rename(filename, new_filepath)
            print(f"Renamed to: {new_filename}")
        else:
            print("Filename is already safe.")

        print("Video downloaded successfully.")

    except Exception as e:
        print("An error occurred while downloading the video:", str(e))

if __name__ == "__main__":
    video_url = sys.argv[1] if len(sys.argv) > 1 else None

    if video_url:
        download_video(video_url)
    else:
        print("Please provide a valid video URL as a command line argument.")

