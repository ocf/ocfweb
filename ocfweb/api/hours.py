from datetime import time
from json import JSONEncoder

from django.http import JsonResponse
from ocflib.lab.hours2 import Hour
from ocflib.lab.hours2 import HoursListing
from ocflib.lab.hours2 import read_hours_listing

from ocfweb.caching import periodic


class JSONHoursEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, HoursListing):
            return obj.__dict__
        elif isinstance(obj, Hour):
            return [obj.open, obj.close]
        elif isinstance(obj, time):
            return obj.strftime('%H:%M:%S')
        else:
            return JSONEncoder.default(self, obj)


@periodic(60)
def get_hours_listing():
    return read_hours_listing()


def get_hours_today(request):
    return JsonResponse(
        get_hours_listing().hours_on_date(),
        encoder=JSONHoursEncoder,
        safe=False,
    )
