from django.http import HttpResponse
from ocflib.account.search import user_attrs
from ocflib.lab.stats import staff_in_lab as real_staff_in_lab

from ocfweb.caching import periodic


@periodic(30)
def _staff_names_in_lab():
    return '\n'.join(sorted(
        user_attrs(user.user)['cn'][0]
        for user in real_staff_in_lab()
    ))


def api_staff_in_lab(request):
    return HttpResponse(
        _staff_names_in_lab(),
        content_type='text/plain',
    )
