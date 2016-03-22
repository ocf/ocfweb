from django.shortcuts import render


def help_index(doc, request):
    return render(
        request,
        'index.html',
        {
            'title': doc.title,
        },
    )
