import os
from yt_dlp import YoutubeDL

def download_video(video_url, output_dir, final_filename_base=None):
    """
    Download the YouTube video using yt_dlp. Return path to the final local file.
    If final_filename_base is given, rename the downloaded file to '{final_filename_base}.mp4'.
    """
    try:
        os.makedirs(output_dir, exist_ok=True)

        ydl_opts = {
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'format': 'best',
            'quiet': True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            original_path = ydl.prepare_filename(info)

        if not os.path.exists(original_path):
            print(f"[!] Could not find downloaded file: {original_path}")
            return None

        # Final rename to match transcript
        if final_filename_base:
            safe_final = f"{final_filename_base}.mp4"
            new_path = os.path.join(output_dir, safe_final)

            # Avoid overwrite
            if os.path.abspath(new_path) != os.path.abspath(original_path):
                os.rename(original_path, new_path)

            return new_path

        return original_path

    except Exception as e:
        print(f"[!] Error downloading video {video_url}: {e}")
        return None
