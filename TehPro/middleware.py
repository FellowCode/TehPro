import pytz

from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from .settings import TIME_ZONE

class TimezoneMiddleware(MiddlewareMixin):
    def process_request(self, request):
        timezone.activate(pytz.timezone(TIME_ZONE))