from django import template
from django.template.defaultfilters import stringfilter

# Custom template filters

register = template.Library()


# Filter concatenating two strings.
@register.filter
@stringfilter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)