from django.shortcuts import render


def docs_index(request):
    return render(
        request,
        'docs/index.html',
        {
            'title': 'Documentation',
        },
    )
