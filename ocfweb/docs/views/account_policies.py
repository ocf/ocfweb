from django.shortcuts import render


def account_policies(doc, request):
    return render(
        request,
        'docs/account-policies.html',
        {
            'title': doc.title,
        },
    )
