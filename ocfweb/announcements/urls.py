from django.conf.urls import url
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.shortcuts import render


def announcement_2016_04_01_renaming(request):
    return render(
        request,
        'announcements/2016-04-01-renaming.html',
        {
            'title': 'Unveiling a new name for the Open Computing Facility',
            'og_title': 'Unveiling a new name for the Open Computing Facility',
            'og_image': request.build_absolute_uri(static('img/announcements/thanks-for-flying-ofc-og.png')),
            'description': (
                'The Board of Directors has voted to rename the Open Computing Facility '
                'to the Open Facility for Computing (OFC).'
            ),
        },
    )


def announcement_2016_02_09_printing(request):
    return render(
        request,
        'announcements/2016-02-09-printing.html',
        {
            'title': 'Changes to printing policies',
        },
    )


urlpatterns = [
    url(r'^2016-02-09/printing$', announcement_2016_02_09_printing, name='printing-announcement'),
    url(r'^2016-04-01/renaming-ocf$', announcement_2016_04_01_renaming, name='renaming-announcement'),
]
