from unittest import mock

import pytest
from django.conf import settings
from django.core.cache import cache
from django.test import Client


@pytest.fixture
def client():
    return Client()


@pytest.yield_fixture(autouse=True)
def in_testing_environment():
    with mock.patch.object(settings, 'TESTING', True):
        yield


def _logged_in_client(user):
    client = Client()
    session = client.session
    session['ocf_user'] = user
    session.save()
    return client


@pytest.fixture
def client_guser():
    return _logged_in_client('guser')


@pytest.fixture
def client_ggroup():
    return _logged_in_client('ggroup')


@pytest.yield_fixture(autouse=True)
def clean_cache():
    with mock.patch(
        'django.conf.settings.CACHES', {
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            },
        },
    ):
        cache.clear()
        yield
