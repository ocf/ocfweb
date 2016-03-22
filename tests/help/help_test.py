import pytest
import requests

from ocfweb.help.urls import DOCS
from tests.end_to_end_test import assert_does_not_error


@pytest.mark.parametrize('doc_name', DOCS.keys())
def test_help_does_not_error(running_server, doc_name):
    assert_does_not_error(running_server, '/help' + doc_name)


@pytest.mark.parametrize('doc_name', ('faq', 'services/lab', 'services/webapps/python'))
def test_docs_redirect_from_docs_to_help(running_server, doc_name):
    """Docs used to be at /docs/ but now are at /help/. We should 301 redirect
    individual docs."""
    for suffix in ('', '/'):
        resp = requests.get(
            running_server + '/docs/' + doc_name + suffix,
            allow_redirects=False,
        )
        assert resp.status_code == 301
        assert resp.headers['Location'] == '/help/' + doc_name + '/'


@pytest.mark.parametrize('path', ['/docs', '/docs/'])
def test_docs_index_redirects_from_docs_to_help(running_server, path):
    """Docs used to be at /docs/ but now are at /help/. We should 301 redirect
    the index page."""
    resp = requests.get(running_server + path, allow_redirects=False)
    assert resp.status_code == 301
    assert resp.headers['Location'] == '/help/'
