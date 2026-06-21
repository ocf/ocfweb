from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render

from ocfweb.component.blog import get_blog_posts
from ocfweb.component.blog import get_news_posts


def announcements(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'main/announcements.html',
        {
            'title': 'News from the staff team',
            'news_posts': get_news_posts()[:10],
            'status_posts': get_blog_posts()[:10],
        },
    )
