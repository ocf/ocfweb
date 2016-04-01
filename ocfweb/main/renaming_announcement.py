from django.contrib.staticfiles.templatetags.staticfiles import static
from django.shortcuts import render


def renaming_announcement(request):
    return render(
        request,
        'renaming-announcement.html',
        {
            'title': 'Unvealing a new name for the Open Computing Facility',
            'og_title': 'Unvealing a new name for the Open Computing Facility',
            'og_image': request.build_absolute_uri(static('img/announcements/thanks-for-flying-ofc-og.png')),
            'description': (
                'The Board of Directors has voted to rename the Open Computing Facility '
                'to the Open Facility for Computing (OFC).'
            ),
        },
    )
