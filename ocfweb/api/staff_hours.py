from json import JSONEncoder

from django.http import JsonResponse

from ocfweb.main.staff_hours import get_staff_hours as real_get_staff_hours


def get_staff_hours(request):
    return JsonResponse(
        list(map(lambda item: item._asdict(), real_get_staff_hours())),
        encoder=JSONEncoder,
        safe=False,
    )
