import re
from os.path import dirname
from os.path import isfile
from os.path import join
from os.path import realpath

from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import redirect

from ocfweb.caching import cache


# images not in PNG that we now redirect to PNG versions
LEGACY_IMAGES = [
    'berknow150x40.jpg',
    'binnov-157x46.gif',
    'lighter152x41.gif',
    'lighter177x48.gif',
    'lighter202x54.gif',
    'metal152x41.gif',
    'metal177x48.gif',
    'metal202x54.gif',
]

HOSTING_LOGOS_PATH = join(dirname(dirname(__file__)), 'static', 'img', 'hosting-logos')


@cache()
def get_image(image):
    match = re.match(r'^[a-z0-9_\-]+\.(png|svg)$', image)
    if not match:
        raise Http404()

    # 'image/png' or 'image/svg'
    content_type = 'image/png' if match.group(1) == 'png' else 'image/svg+xml'

    path = join(HOSTING_LOGOS_PATH, image)

    # sanity check that the file is under the directory we expect
    assert path.startswith(realpath(HOSTING_LOGOS_PATH) + '/')

    if not isfile(path):
        raise Http404()

    with open(path, 'rb') as f:
        return f.read(), content_type


def hosting_logo(request, image):
    """Hosting logos must be served from the root since they are linked by
    student group websites."""
    # legacy images
    if image in LEGACY_IMAGES:
        return redirect('hosting-logo', re.sub('\.[a-z]+$', '.png', image), permanent=True)

    content, content_type = get_image(image)
    return HttpResponse(
        content,
        content_type=content_type,
    )
