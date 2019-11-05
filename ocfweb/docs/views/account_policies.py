from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render

from ocfweb.docs.doc import Document


def account_policies(doc: Document, request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'docs/account_policies.html',
        {
            'title': doc.title,
        },
    )
