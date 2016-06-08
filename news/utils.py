from html.parser import HTMLParser

# === Utils for news app ===


class MLStripper(HTMLParser):
    """

    This MLStripper class represents an HTML parser.

    """

    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_html_tags(html):
    """

    The find_first_after_n function takes one parameter:

    1. **html** - input string


    The function returns the the input string with all of the HTML tags deleted.

    """
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def find_first_after_n(haystack, needle, n):
    """

    The find_first_after_n function takes three parameters:

    1. **haystack** - string, in which the needle should be searched for
    2. **needle** - substring to search for
    2. **n** - defines the number of characters, after which the needle should be searched for

    The function returns the index of the first occurrence of the needle after n characters and -1 if it was not found.
    For example: for input: haystack == 'abcdab', needle == 'a', n == 2, 4 will be returned

    """
    if n >= len(haystack):
        return -1
    end_substr = haystack[n:]
    occurenece_index = end_substr.find(needle)
    if occurenece_index == -1:
        return -1
    return occurenece_index + n


def shorten_content(content, n):
    """

    The youtube_video_exists function takes two parameters:

    1. **content** - string with the content of an article possibly containing formatting
    2. **n** - number of characters at the beginning of the content that are guaranteed to be preserved

    The function returns the content shortened to around n characters.
    All HTML tags are gone.
    If the content was too long to be shortened, the string itself will be returned.
    If shortening occurred, an ellipsis will be added.

    """
    content_without_html = strip_html_tags(content)
    if len(content_without_html) < n:
        return content_without_html
    first_whitespace_after_n = find_first_after_n(content_without_html, ' ', n)
    if first_whitespace_after_n == -1:
        return content_without_html
    return content_without_html[:first_whitespace_after_n] + '...'






