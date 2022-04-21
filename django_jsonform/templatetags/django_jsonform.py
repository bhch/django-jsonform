from django import template
from django.utils import timezone
from datetime import time


register = template.Library()


@register.filter
def parse_datetime(value):
    """Converts ISO date string to a datetime object
    which can be used with the ``date`` filter.
    """
    return timezone.datetime.fromisoformat(value)


@register.filter
def parse_time(value):
    """Converts a time string (24-hour format) to a time object
    whch can be used with the ``time`` filter.
    """
    return time(*[int(x) for x in value.split(':')])
