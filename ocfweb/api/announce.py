from typing import Any

from django.http import JsonResponse

from ocfweb.component.blog import get_blog_posts as real_get_blog_posts


def get_blog_posts(request: Any) -> JsonResponse:
    return JsonResponse(
        [item._asdict() for item in real_get_blog_posts()],
        safe=False,
    )
