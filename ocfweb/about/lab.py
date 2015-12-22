from django.shortcuts import render


def lab_open_source(request):
    return render(
        request,
        'lab-open-source.html',
        {
            'title': 'Open Source in our Computer Lab',
        },
    )
