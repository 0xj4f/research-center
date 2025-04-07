from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import requests
import os

def fetch_video_metadata(video_id):
    """
    Use oEmbed to fetch basic video metadata (title, author).
    Return dict {'title': ..., 'author': ...}. 
    """
    url = f"https://www.youtube.com/oembed?url=http://www.youtube.com/watch?v={video_id}&format=json"
    try:
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            title = data.get('title', 'Unknown_Title')
            author = data.get('author_name', 'Unknown_Author')
            return {"title": title, "author": author}
        else:
            print(f"[!] Error fetching metadata for {video_id}, status: {r.status_code}")
    except Exception as e:
        print(f"[!] Exception fetching metadata: {e}")

    return {"title": "Unknown_Title", "author": "Unknown_Author"}

def download_transcript(video_id):
    """
    Attempt to fetch the English transcript from youtube_transcript_api.
    Return the combined text or None if not available.
    """
    try:
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        transcript_text = ' '.join(segment['text'] for segment in transcript_data)
        return transcript_text
    except TranscriptsDisabled:
        print(f"[!] Transcripts disabled for {video_id}")
    except NoTranscriptFound:
        print(f"[!] No transcript found for {video_id}")
    except Exception as e:
        print(f"[!] Error retrieving transcript for {video_id}: {e}")
    return None

def save_transcript(transcript, output_dir, base_filename):
    """
    Save the transcript as {base_filename}.txt in output_dir.
    """
    if not transcript:
        return None

    os.makedirs(output_dir, exist_ok=True)
    txt_path = os.path.join(output_dir, f"{base_filename}.txt")
    try:
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(transcript)
        print(f"[+] Transcript saved to {txt_path}")
        return txt_path
    except Exception as e:
        print(f"[!] Error saving transcript: {e}")
        return None
