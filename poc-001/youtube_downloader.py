import os
import sys
import pytube

"""
pip install pytube
"""

def download_video(video_url):
    try:
        # Define output directory
        output_dir = "./youtube-videos"
        os.makedirs(output_dir, exist_ok=True)

        youtube = pytube.YouTube(video_url)
        video_stream = youtube.streams.get_highest_resolution()
        downloaded_path = video_stream.download(output_path=output_dir)

        # Rename file to replace spaces with dashes
        original_filename = os.path.basename(downloaded_path)
        new_filename = original_filename.replace(" ", "-")
        new_filepath = os.path.join(output_dir, new_filename)

        os.rename(downloaded_path, new_filepath)

        print(f"Downloading {original_filename}")
        print("Video downloaded successfully.")
    except Exception as e:
        print("An error occurred while downloading the video:", str(e))

if __name__ == "__main__":
    video_url = sys.argv[1] if len(sys.argv) > 1 else None

    if video_url:
        download_video(video_url)
    else:
        print("Please provide a valid video URL as a command line argument.")

import os
import sys
from pytube import YouTube

def download_video(video_url):
    try:
        youtube = YouTube(video_url)
        video_stream = youtube.streams.get_highest_resolution()
        original_filename = video_stream.default_filename

        print(f"Downloading: {original_filename}")
        video_stream.download()

        safe_filename = original_filename.replace(" ", "-")
        if original_filename != safe_filename:
            os.rename(original_filename, safe_filename)
            print(f"Renamed to: {safe_filename}")
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


import sys
from pytube import YouTube

def download_video(video_url):
    try:
        yt = YouTube(video_url)
        stream = yt.streams.get_highest_resolution()

        print(f"Downloading: {yt.title}")
        stream.download()
        print("Download complete.")
    except Exception as e:
        print("Download failed:", str(e))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 youtube_downloader.py <youtube_url>")
        sys.exit(1)

    download_video(sys.argv[1])
