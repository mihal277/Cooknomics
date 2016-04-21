from django.utils import timezone


def one_day_hence():
    return timezone.now() + timezone.timedelta(days=1)
