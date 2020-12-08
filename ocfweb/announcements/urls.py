from django.conf.urls import url

from ocfweb.announcements.announcements import announcements
from ocfweb.announcements.announcements import index


urlpatterns = [
    url(r'^$', index, name='announcements'),
] + [
    url(
        f'^{announcement.date.isoformat()}/{announcement.path}$',
        announcement.render,
        name=announcement.route_name,
    )
    for announcement in announcements
]
