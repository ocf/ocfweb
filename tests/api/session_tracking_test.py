import json
from unittest import mock

import pytest
from django.urls import reverse

from ocfweb.api import session_tracking
from ocfweb.api.session_tracking import log_session

# something we know is a desktop or VM
OCF_DESKTOP_IP = '169.229.226.118'
OCF_DESKTOP_HOST = 'blackout.ocf.berkeley.edu'
OCF_VM_IP = '169.229.226.36'


def test_view_requires_post(client):
    """Ensure that GETs return Method Not Allowed."""

    resp = client.get(reverse(log_session))
    assert resp.status_code == 405


TEST_SOURCE_IPS = (
    (OCF_DESKTOP_IP, 400, ''),  # valid IP but invalid data == 400
    (OCF_VM_IP, 400, 'IP {} does not belong to a desktop'.format(OCF_VM_IP)),
    ('169.229.228.90', 401, 'Not Authorized'),
    ('8.8.8.8', 401, 'Not Authorized'),
    ('1.10.11.12', 401, 'Not Authorized'),
)


@pytest.mark.parametrize('source', TEST_SOURCE_IPS)
def test_view_requires_ocf_ip(source, client):
    """Only accept OCF IPs and check against provided error message."""

    ip, status, body = source
    resp = client.post(reverse(log_session), REMOTE_ADDR=ip)
    assert resp.status_code == status
    assert resp.content.decode('utf-8').startswith(body)


TEST_INVALID_POST_DATA = (
    # valid user, invalid state
    ({'user': 'guser', 'state': 'inactive'}, "'inactive'"),
    ({'user': 'guser', 'state': 'foo'}, "'foo'"),
    # invalid user, valid state
    ({'user': '', 'state': 'active'}, 'No user specified'),
    ({'user': '', 'state': 'cleanup'}, 'No user specified'),
    # invalid everything
    ({'user': '', 'state': 'inactive'}, "'inactive'"),
    ({'user': '', 'state': 'foo'}, "'foo'"),
)


@pytest.mark.parametrize('data', TEST_INVALID_POST_DATA)
def test_failure_on_invalid_data(client, data):
    """Test for failure when invalid data is POSTed to the endpoint.

    Invalid state raises a KeyError, and invalid usernames ValueError,
    both of which are caught and return HTTP 400.
    """
    data, body = data
    resp = client.post(
        reverse(log_session),
        json.dumps(data),
        content_type='application/json',
        REMOTE_ADDR=OCF_DESKTOP_IP,
    )
    assert resp.status_code == 400
    assert resp.content.decode('utf-8').startswith(body)


@pytest.fixture
def mock_new_session():
    with mock.patch.object(session_tracking, '_new_session') as m:
        yield m


@pytest.fixture
def mock_session_exists():
    with mock.patch.object(session_tracking, '_session_exists') as m:
        yield m


@pytest.fixture
def mock_refresh_session():
    with mock.patch.object(session_tracking, '_refresh_session') as m:
        yield m


@pytest.fixture
def mock_close_sessions():
    with mock.patch.object(session_tracking, '_close_sessions') as m:
        yield m


TEST_SESSION_VALID_DATA = {'user': 'guser', 'state': 'active'}
TEST_SESSION_VALID_CLEANUP = {'user': 'guser', 'state': 'cleanup'}


def test_create_new_session(
    client,
    mock_new_session,
    mock_refresh_session,
    mock_close_sessions,
):
    """Test that a new session is made if one doesn't already exist."""

    with mock.patch.object(session_tracking, '_session_exists', return_value=False):
        resp = client.post(
            reverse(log_session),
            json.dumps(TEST_SESSION_VALID_DATA),
            content_type='application/json',
            REMOTE_ADDR=OCF_DESKTOP_IP,
        )

        mock_new_session.assert_called_once_with(
            OCF_DESKTOP_HOST,
            TEST_SESSION_VALID_DATA['user'],
        )

        assert resp.status_code == 204
        mock_refresh_session.assert_not_called()
        mock_close_sessions.assert_not_called()


def test_refresh_session(
    client,
    mock_refresh_session,
    mock_new_session,
    mock_close_sessions,
):
    """Test that if a session exists, it gets refreshed, and nothing else."""

    with mock.patch.object(session_tracking, '_session_exists', return_value=True):
        resp = client.post(
            reverse(log_session),
            json.dumps(TEST_SESSION_VALID_DATA),
            content_type='application/json',
            REMOTE_ADDR=OCF_DESKTOP_IP,
        )

        mock_refresh_session.assert_called_once_with(
            OCF_DESKTOP_HOST,
            TEST_SESSION_VALID_DATA['user'],
        )

        assert resp.status_code == 204
        mock_new_session.assert_not_called()
        mock_close_sessions.assert_not_called()


def test_close_session(
    client,
    mock_close_sessions,
    mock_refresh_session,
    mock_session_exists,
    mock_new_session,
):
    """Test that on receiving state=cleanup, sessions are closed, and nothing else."""

    resp = client.post(
        reverse(log_session),
        json.dumps(TEST_SESSION_VALID_CLEANUP),
        content_type='application/json',
        REMOTE_ADDR=OCF_DESKTOP_IP,
    )

    mock_close_sessions.assert_called_once_with(
        OCF_DESKTOP_HOST,
    )

    assert resp.status_code == 204
    mock_new_session.assert_not_called()
    mock_refresh_session.assert_not_called()
    mock_session_exists.assert_not_called()
