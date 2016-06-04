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


def validate_image(size, name):
    """

    The function first validates the format of the file. Then the size.
    If any of these fails, ValidationError is raised.

    """
    if not name.endswith((".jpg", ".png", "jpeg")):
        raise ValidationError(".jpg, .png or .jpeg format required")

    megabyte_limit = 3.0
    if size > megabyte_limit * 1024 * 1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))






