import requests
import json
import urllib.request
#from lxml import etree

# === Utils for videos app ===


def get_youtube_video_title(video_url):
    """

    The get_youtube_video_title function takes one parameter:

    1. **video_url** - the URL of a youtube video

    The function extracts and returns the title of the video, which gets downloaded from youtube

    """
    youtube_api_url = 'https://www.youtube.com/oembed?url=' + video_url
    response = requests.get(youtube_api_url)
    json_data = json.loads(response.text)
    return json_data['title']


def get_youtube_video_description(video_url):
    """

    The get_youtube_video_description function takes one parameter:

    1. **video_url** - the URL of a youtube video

    The function extracts and returns the description of the video, which gets downloaded from youtube

    """
    #with urllib.request.urlopen(video_url) as response:
        #video_page_source = etree.HTML(response.read())
    #return str(video_page_source.xpath("//p[@id='eow-description']/text()"))[2:-2]
    return "no description"


def youtube_video_exists(video_url):
    """

    The youtube_video_exists function takes one parameter:

    1. **video_url** - the URL of a youtube video

    The function return true if the video_url contains a correct video and false otherwise.

    """
    youtube_api_url = 'https://www.youtube.com/oembed?url=' + video_url
    response = requests.get(youtube_api_url)
    if response.status_code == 404:
        return False
    return True


def trim_youtube_url(video_url):
    """

    The trim_youtube_url function takes one parameter:

    1. **video_url** - the URL of a youtube video

    The function returns the unique identifier of the video.

    """

    return video_url.split("v=")[1]
