from django.shortcuts import render


def docs_index(request):
    return render(
        request,
        'index.html',
        {
            'title': 'Documentation',
        },
    )
