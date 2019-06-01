from django.shortcuts import render


def docs_index(request):
    return render(
        request,
        'docs/index.html',
        {
            'title': 'Documentation',
        },
    )


def staffdocs_index(request):
    return render(
        request,
        'docs/staff_index.html',
        {
            'title': 'Staff Documentation',
        },
    )
