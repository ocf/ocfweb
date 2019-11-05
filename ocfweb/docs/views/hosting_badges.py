from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

from ocfweb.docs.doc import Document


def hosting_badges(doc: Document, request: HttpRequest) -> HttpResponse:
    badges = [
        (name, request.build_absolute_uri(reverse('hosting-logo', args=(name,))))
        for name in [
            'ocf-hosted-penguin.svg',
            'ocf-hosted-penguin-dark.svg',
            'ocfbadge_silver8.png',
            'ocfbadge_blue8.png',
        ]
    ]

    return render(
        request,
        'docs/hosting_badges.html',
        {
            'title': doc.title,
            'badges': badges,
        },
    )
