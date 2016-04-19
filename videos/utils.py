import random
import string


def random_url_populate(value):
    """Returns a random slug consisting of upper-case letters,
    lower-case letters and numbers

    TODO: filter offensive words
    """
    return ''.join(random.sample(string.ascii_uppercase +
                                 string.ascii_lowercase +
                                 string.digits, 7))

