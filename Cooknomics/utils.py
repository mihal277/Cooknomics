from django.utils import timezone
from django.core.exceptions import ValidationError


def one_day_hence():
    return timezone.now() + timezone.timedelta(days=1)


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
