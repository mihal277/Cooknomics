from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import urllib.request as req

# === Utils for partners app ===


def validate_url(url):
    """

    The function first validates the formatting of the url and then tries to open the link.
    If any of these fails, ValidationError is raised.

    """
    val = URLValidator()
    try:
        val(url)
    except ValidationError:
        raise ValidationError("Wrong url. Correct format: http://www.page.com/")

    request = req.Request(url)
    try:
        req.urlopen(request)
    except:
        raise ValidationError("Wrong url. Cannot connect to this page")







