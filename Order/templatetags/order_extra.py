from django import template
from django.conf import settings

import pytz

register = template.Library()

@register.filter
def astimezone(date, destination=None):

    if not destination:
        destination = settings.TIME_ZONE

    if date.tzinfo:
        return date.astimezone(pytz.timezone(destination))
    else:
        return pytz.timezone(settings.TIME_ZONE).localize(date).astimezone(pytz.timezone(destination))
