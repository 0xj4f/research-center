from argparse import ArgumentParser
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from pytube import YouTube
import os
import requests

"""
pip3 install pytube youtube-transcript-api
"""

def parse_arguments():
    parser = ArgumentParser(description="Download YouTube transcripts.")
    parser.add_argument('-f', '--file', help="Path to a file containing YouTube URLs, one per line.")
    parser.add_argument('-u', '--url', help="A single YouTube URL.")
    return parser.parse_args()

def download_transcript(url):
    video_id = url.split("v=")[1]
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        transcript = ' '.join([segment['text'] for segment in transcript_list])
        return transcript
    except TranscriptsDisabled:
        print(f"Transcripts are disabled for video: {url}")
    except NoTranscriptFound:
        print(f"No transcript found for video: {url}")
    except Exception as e:
        print(f"Error downloading transcript for {url}: {e}")
    return None

# def fetch_video_metadata(video_id):
#     video_url = f'https://www.youtube.com/watch?v={video_id}'
#     yt = YouTube(video_url)
    
#     title = yt.title
#     author = yt.author
#     publish_date = yt.publish_date.strftime('%Y-%m-%d') if yt.publish_date else "Unknown Date"
    
#     return {
#         "title": title,
#         "author": author,
#         "upload_date": publish_date
#     }

def fetch_video_metadata(video_id):
    url = f"https://www.youtube.com/oembed?url=http://www.youtube.com/watch?v={video_id}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        title = data.get('title', 'Unknown Title')
        author = data.get('author_name', 'Unknown Author')
        upload_date = "Unknown Date"  # oEmbed doesn't provide upload date
    else:
        print(f"Error fetching video metadata: {response.status_code}")
        title = 'Unknown Title'
        author = 'Unknown Author'
        upload_date = 'Unknown Date'
    return {
        "title": title,
        "author": author,
        "upload_date": upload_date
    }
    
def generate_filename(metadata):
    title = metadata['title'].replace(" ", "_").replace("/", "_")
    author = metadata['author'].replace(" ", "_").replace("/", "_")
    upload_date = metadata['upload_date']
    return f"{title}-{author}-{upload_date}.txt"

def save_output_to_file(output, metadata, directory="./youtube-transcripts/"):
    if not output:
        print("[-] No output to save")
        return
    
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    
    filename = generate_filename(metadata)
    filepath = os.path.join(directory, filename)
    with open(filepath, 'w') as file:
        file.write(output)
    print(f"[+] Output saved to {filepath}")

def main():
    args = parse_arguments()
    youtube_urls = []

    if args.file:
        with open(args.file, 'r') as file:
            youtube_urls = file.read().splitlines()
    elif args.url:
        youtube_urls.append(args.url)
    
    for url in youtube_urls:
        transcript = download_transcript(url)
        if transcript:
            video_id = url.split("v=")[1]
            metadata = fetch_video_metadata(video_id)
            save_output_to_file(transcript, metadata)

if __name__ == "__main__":
    main()
