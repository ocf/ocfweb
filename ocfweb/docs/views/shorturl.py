from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render

from ocfweb.docs.doc import Document


def shorturl(doc: Document, request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'docs/shorturl.html',
        {
            'title': doc.title,
        },
    )
