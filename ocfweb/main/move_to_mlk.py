from django.shortcuts import render


def move_to_mlk(request):
    return render(
        request,
        'move-to-mlk.html',
        {
            'title': 'Move to MLK Student Union (Fall 2015)',
        },
    )
