import requests

# === Utils for videos app ===


def youtube_video_exists(video_url):
    """

    The youtube_video_exists takes one parameter:

    1. **video_url** - the URL of a youtube video

    The function return true if the video_url contains a correct video and false otherwise.

    """
    youtube_api_url = 'https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=' + video_url
    response = requests.get(youtube_api_url)
    if response.status_code == 404:
        return False
    return True
