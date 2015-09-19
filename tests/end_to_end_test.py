from textwrap import dedent

import pytest
import requests
from django.core.urlresolvers import NoReverseMatch
from django.core.urlresolvers import reverse

from ocfweb.docs.docs import list_doc_names
from ocfweb.urls import urlpatterns


def _assert_does_not_error(running_server, path):
    path = running_server + path
    resp = requests.get(path)
    if resp.status_code != 200:
        raise AssertionError(
            dedent('''\
            Should have received status code 200, but instead received {resp.status_code}.

            Full path: {path}

            The response body was:
            {resp.content}''').format(path=path, resp=resp)
        )


def _get_reversed_urlpatterns():
    """Yields a list of all URLs that we can reverse with default args."""
    for urlpattern in urlpatterns:
        try:
            path = reverse(urlpattern.name, *urlpattern.default_args)
        except NoReverseMatch:
            pass
        else:
            yield path


@pytest.mark.parametrize('path', _get_reversed_urlpatterns())
def test_view_does_not_error_with_default_args(running_server, path):
    _assert_does_not_error(running_server, path)


@pytest.mark.parametrize('doc_name', list_doc_names())
def test_doc_does_not_error(running_server, doc_name):
    _assert_does_not_error(running_server, '/docs' + doc_name)
