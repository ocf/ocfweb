from django.urls import re_path

from ocfweb.lab_reservations.reserve import request_reservation
from ocfweb.lab_reservations.reserve import request_reservation_success


urlpatterns = [
    # reservation creation form
    re_path(r'^request/$', request_reservation, name='request_reservation'),

    # reservation pending
    re_path(r'^request/pending/$', request_reservation_success, name='request_reservation_success'),
]
