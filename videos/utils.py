import random
import string
import requests


def random_url_populate(*args):
    """Returns a random slug consisting of upper-case letters,
    lower-case letters and numbers

    TODO: filter offensive words
    """
    return ''.join(random.sample(string.ascii_uppercase +
                                 string.ascii_lowercase +
                                 string.digits, 7))


def youtube_video_exists(video_url):
    youtube_api_url = 'https://www.youtube.com/oembed?url=' + video_url
    response = requests.get(youtube_api_url)
    if response.status_code == 404:
        return False
    return True

