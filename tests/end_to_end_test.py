from textwrap import dedent

import pytest
from django.core.urlresolvers import NoReverseMatch
from django.core.urlresolvers import RegexURLPattern
from django.core.urlresolvers import RegexURLResolver
from django.core.urlresolvers import reverse

from ocfweb.urls import urlpatterns


def assert_does_not_error(client, path):
    resp = client.get(path, follow=True)
    if resp.status_code != 200:
        # If a SERVER_NAME is set, then we redirect off-site (e.g. to CAS).
        # We'll just assume those would have succeeded.
        if 'SERVER_NAME' not in resp.request:
            raise AssertionError(
                dedent('''\
                Should have received status code 200, but instead received {resp.status_code}.

                Full path: {path}
                Final URL: {resp.url}

                The response body was:
                {resp.content}''').format(path=path, resp=resp)
            )


def _get_reversed_urlpatterns(urlpatterns=urlpatterns):
    """Yields a list of all URLs that we can reverse with default args."""
    for urlpattern in urlpatterns:
        if isinstance(urlpattern, RegexURLPattern):
            try:
                path = reverse(urlpattern.name, *urlpattern.default_args)
            except NoReverseMatch:
                pass
            else:
                yield path
        elif isinstance(urlpattern, RegexURLResolver):
            # handle recursive urlpattern definitions
            yield from _get_reversed_urlpatterns(urlpatterns=urlpattern.url_patterns)


@pytest.mark.parametrize('path', _get_reversed_urlpatterns())
def test_view_does_not_error_with_default_args(client, path):
    assert_does_not_error(client, path)
