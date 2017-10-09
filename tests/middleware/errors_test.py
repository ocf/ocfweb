from ocfweb.middleware import errors


def test_sanitize():
    assert errors.sanitize(
        "'a': True, 'encrypted_password': b'asdf',",
    ) == "'a': True, 'encrypted_password': b'<REDACTED>',"


def test_sanitize_wsgi_context():
    assert errors.sanitize_wsgi_context({
        'CONTENT_LENGTH': 123,
        'HTTP_CONNECTION': 'close',
        'CSRF_COOKIE': 'secret',
        'HTTP_COOKIE': 'secret',
        'wsgi.version': (1, 0),
    }) == {
        'CONTENT_LENGTH': 123,
        'HTTP_CONNECTION': 'close',
        'CSRF_COOKIE': '<REDACTED>',
        'HTTP_COOKIE': '<REDACTED>',
        'wsgi.version': (1, 0),
    }
