from django.urls import re_path

from ocfweb.announcements.announcements import announcements
from ocfweb.announcements.announcements import index


urlpatterns = [
    re_path(r'^$', index, name='announcements'),
] + [
    re_path(
        f'^{announcement.date.isoformat()}/{announcement.path}$',
        announcement.render,
        name=announcement.route_name,
    )
    for announcement in announcements
]
