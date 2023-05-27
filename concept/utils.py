import pafy

def fetch_thumbnail(youtube_url):
    try:
        video = pafy.new(youtube_url)
        thumbnail_url = video.bigthumb
        return thumbnail_url
    except Exception as e:
        # Handle any exceptions that occur during retrieval
        print(f"Error fetching thumbnail for video: {youtube_url}. Error: {str(e)}")
        return None
