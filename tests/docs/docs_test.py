import pytest

from ocfweb.docs.urls import DOCS
from tests.end_to_end_test import assert_does_not_error


@pytest.mark.parametrize('doc_name', DOCS.keys())
def test_doc_does_not_error(running_server, doc_name):
    assert_does_not_error(running_server, '/docs' + doc_name)
