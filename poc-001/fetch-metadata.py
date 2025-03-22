import requests

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

if __name__ == "__main__":
    fetch_video_metadata()