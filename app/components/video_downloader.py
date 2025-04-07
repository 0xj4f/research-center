# components/video_downloader.py
import os
from yt_dlp import YoutubeDL
import datetime

def download_video(video_url, output_dir):
    """
    Download the YouTube video via yt_dlp. 
    Return the local path of the final downloaded file.
    """
    try:
        os.makedirs(output_dir, exist_ok=True)

        ydl_opts = {
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'format': 'best',
            'quiet': True,   # Set to False if you want verbose logs
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)

        # Replace spaces with dashes or underscores
        base_dir, original_filename = os.path.split(filename)
        safe_filename = original_filename.replace(" ", "-")
        new_filepath = os.path.join(base_dir, safe_filename)

        if original_filename != safe_filename:
            os.rename(filename, new_filepath)
            # print(f"Renamed to: {safe_filename}")

        return new_filepath

    except Exception as e:
        print(f"An error occurred while downloading the video {video_url}: {e}")
        return None
