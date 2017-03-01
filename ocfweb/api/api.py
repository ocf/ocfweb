from django.http import JsonResponse
from ocflib.lab.hours import Day


def sign_text(request):
    today = Day.from_date()
    dic = {
        'date': today.date,
        'day': today.weekday,
        'holiday': today.holiday,
        'hours': today.hours
    }

    return JsonResponse(dic,
                        json_dumps_params={'default': lambda x: x.isoformat()},
                        content_type='application/json')
