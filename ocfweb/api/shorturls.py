from typing import Any
from typing import Union

from django.http import HttpResponseNotFound
from django.http import HttpResponseRedirect
from ocflib.misc.shorturls import get_connection
from ocflib.misc.shorturls import get_shorturl


def bounce_shorturl(request: Any, slug: Any) -> Union[HttpResponseRedirect, HttpResponseNotFound]:
    if slug:
        with get_connection() as ctx:
            target = get_shorturl(ctx, slug)

        if target:
            return HttpResponseRedirect(target)

    return HttpResponseNotFound()
