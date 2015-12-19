import random
import socket
import subprocess
import sys
import time

import mock
import pytest
import requests
from django.core.cache import cache


@pytest.yield_fixture(autouse=True)
def clean_cache():
    with mock.patch('django.conf.settings.CACHES', {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        },
    }):
        cache.clear()
        yield


@pytest.fixture(scope='session')
def unused_port():
    def used(port):
        s = socket.socket()
        try:
            s.bind(('127.0.0.1', port))
        except Exception:
            return True
        else:
            s.close()
            return False

    port = None
    while port is None or used(port):
        port = random.randint(10000, 65535)

    return port


@pytest.yield_fixture(scope='session')
def running_server(unused_port):
    """Start a running ocfweb instance.

    Yields a prefix like "http://localhost:1234".

    Example usage:
    assert requests.get(running_server + '/status').status_code == 200
    """
    # we'd like to use unix sockets here, but they are poorly supported by
    # requests (and the third-party requests-unixsocket module is buggy)
    proc = subprocess.Popen((
        sys.executable,
        '-m', 'gunicorn.app.wsgiapp',
        '-b', '127.0.0.1:' + str(unused_port),
        'ocfweb.wsgi',
    ))
    prefix = 'http://127.0.0.1:' + str(unused_port)

    start = time.time()
    while time.time() - start < 5:
        try:
            if requests.get(prefix + '/_status').status_code == 200:
                break
        except requests.exceptions.ConnectionError:
            pass

        time.sleep(0.1)
    else:
        raise TimeoutError('Unable to start ocfweb within 5 seconds.')

    yield prefix

    proc.terminate()
    proc.wait()
    assert proc.returncode == 0
