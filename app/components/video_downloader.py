import os
from yt_dlp import YoutubeDL

def download_video(video_url, output_dir, final_filename_base=None):
    """
    Download the YouTube video using yt_dlp. Return path to the final local file.
    If final_filename_base is given, rename the final file to '{final_filename_base}.mp4'.
    """
    try:
        os.makedirs(output_dir, exist_ok=True)

        ydl_opts = {
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'format': 'best',   # or 'bestvideo+bestaudio/best'
            'quiet': True,      # set to False for more verbose logs
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            original_path = ydl.prepare_filename(info)

        if not os.path.exists(original_path):
            print(f"[!] Could not find downloaded file: {original_path}")
            return None

        if final_filename_base:
            # rename to e.g. {final_filename_base}.mp4
            base_dir = os.path.dirname(original_path)
            new_filename = f"{final_filename_base}.mp4"
            new_filepath = os.path.join(base_dir, new_filename)

            os.rename(original_path, new_filepath)
            return new_filepath
        else:
            # fallback, no special rename
            return original_path

    except Exception as e:
        print(f"[!] Error downloading video {video_url}: {e}")
        return None
