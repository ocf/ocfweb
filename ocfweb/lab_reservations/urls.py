from django.conf.urls import url

from ocfweb.lab_reservations.reserve import request_reservation
from ocfweb.lab_reservations.reserve import reservation_requested


urlpatterns = [

    # reservation creation form
    url(r'^request/$', request_reservation, name='request_reservation'),

    # reservation pending
    url(r'^request/pending/$', reservation_requested, name='reservation_requested'),

]
