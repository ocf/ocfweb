from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render


def test_shorturl(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'test/shorturl.html',
        {
            'title': 'OCF ShortURLs',
        },
    )
