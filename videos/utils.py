import requests


def youtube_video_exists(video_url):
    youtube_api_url = 'https://www.youtube.com/oembed?url=' + video_url
    response = requests.get(youtube_api_url)
    if response.status_code == 404:
        return False
    return True

