from django.shortcuts import render


def printing_announcement(request):
    return render(
        request,
        'printing-announcement.html',
        {
            'title': 'Changes to printing policies',
        },
    )
