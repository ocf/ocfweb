from django.shortcuts import render


def account_policies(doc, request):
    return render(
        request,
        'docs/account_policies.html',
        {
            'title': doc.title,
        },
    )
