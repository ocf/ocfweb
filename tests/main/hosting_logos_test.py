import pytest


@pytest.mark.parametrize('path', [
    '/images/hosted-logos/',
    '/hosting-logos/',
])
@pytest.mark.parametrize('image', [
    'berknow150x40.jpg',
    'berknow150x40.png',
    'binnov-157x46.gif',
    'binnov-157x46.png',
    'lighter152x41.gif',
    'lighter152x41.png',
    'lighter177x48.gif',
    'lighter177x48.png',
    'lighter202x54.gif',
    'lighter202x54.png',
    'metal152x41.gif',
    'metal152x41.png',
    'metal177x48.gif',
    'metal177x48.png',
    'metal202x54.gif',
    'metal202x54.png',
    'ocf-hosting-flag-wave-250x122.png',
    'ocfbadge_blue8.png',
    'ocfbadge_mini8.png',
    'ocfbadge_mini8dark.png',
    'ocfbadge_mini8darkglow.png',
    'ocfbadge_platinum.png',
    'ocfbadge_silver8.png',
])
def test_images_load(path, image, client):
    """This is a sanity check that old and new images all eventually load.

    I know, it looks silly to list them all above. But we want to be extra
    careful we don't accidentally break old links by removing images we think
    are unused, hence we duplicate them in tests.
    """
    resp = client.get(path + image, follow=True)
    assert resp.status_code == 200
    assert resp.get('Content-Type') == 'image/png'


@pytest.mark.parametrize('path', [
    '/images/hosted-logos/',
    '/hosting-logos/',
])
@pytest.mark.parametrize('image', [
    'ocf-hosted-penguin.svg',
])
def test_svg_images_load(path, image, client):
    """This is the same sanity check as test_images_load, but checks SVGs
    separately to make sure they return the right MIME type."""
    resp = client.get(path + image, follow=True)
    assert resp.status_code == 200
    assert resp.get('Content-Type') == 'image/svg+xml'


@pytest.mark.parametrize('image', [
    'berknow150x40.jpg',
    'binnov-157x46.gif',
    'lighter152x41.gif',
    'lighter177x48.gif',
    'lighter202x54.gif',
    'metal152x41.gif',
    'metal177x48.gif',
    'metal202x54.gif',
])
def test_legacy_images_redirect(image, client):
    """Legacy images (non-PNG) should redirect to the PNG versions."""
    resp = client.get('/hosting-logos/' + image, allow_redirects=False)
    assert resp.status_code == 301
    assert resp.get('Location').endswith('.png')
