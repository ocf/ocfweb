from django.shortcuts import render


def servers(doc, request):
    return render(
        request,
        'servers.html',
        {
            'title': doc.title,
        },
    )
