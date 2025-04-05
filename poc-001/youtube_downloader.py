import os
import sys
import pytube
"""
pip install pytube
"""
def download_video(video_url):
    try:
        youtube = pytube.YouTube(video_url)
        video_stream = youtube.streams.get_highest_resolution()
        video_stream.download()

        original_filename = video_stream.default_filename
        print(f"Downloading {original_filename}")
        os.rename(original_filename, original_filename.replace(" ", "-"))

        print("Video downloaded successfully.")
    except Exception as e:
        print("An error occurred while downloading the video:", str(e))

if __name__ == "__main__":
    video_url = sys.argv[1] if len(sys.argv) > 1 else None

    if video_url:
        download_video(video_url)
    else:
        print("Please provide a valid video URL as a command line argument.")
