# components/transcript_downloader.py
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import requests
import os
import re

def download_transcript(video_id):
    """
    Attempt to download the English transcript by video_id.
    Return the transcript text or None if not found/disabled.
    """
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        transcript = ' '.join([seg['text'] for seg in transcript_list])
        return transcript
    except TranscriptsDisabled:
        print(f"Transcripts disabled for video ID: {video_id}")
    except NoTranscriptFound:
        print(f"No transcript found for video ID: {video_id}")
    except Exception as e:
        print(f"Error: {e}")
    return None

def fetch_video_metadata(video_id):
    """
    Uses oEmbed to fetch basic metadata (title, author).
    No guaranteed date from oEmbed, so returns 'Unknown Date'.
    """
    url = f"https://www.youtube.com/oembed?url=http://www.youtube.com/watch?v={video_id}&format=json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            title = data.get('title', 'UnknownTitle')
            author = data.get('author_name', 'UnknownAuthor')
            upload_date = 'UnknownDate'  # not provided by oembed
            return {
                "title": title,
                "author": author,
                "upload_date": upload_date
            }
        else:
            print(f"Error fetching metadata for {video_id}: {response.status_code}")
    except Exception as e:
        print(f"Error fetching metadata: {e}")

    return {
        "title": "UnknownTitle",
        "author": "UnknownAuthor",
        "upload_date": "UnknownDate"
    }

def save_transcript(transcript, metadata, output_dir):
    """
    Save transcript to a .txt file in 'output_dir', 
    naming by sanitized title-author.
    """
    if not transcript:
        return

    os.makedirs(output_dir, exist_ok=True)

    title = metadata['title'].replace(" ", "_")
    author = metadata['author'].replace(" ", "_")
    # We'll skip upload_date since it's "UnknownDate" anyway from oembed

    filename = f"{title}-{author}.txt"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(transcript)

    print(f"Transcript saved to: {filepath}")
