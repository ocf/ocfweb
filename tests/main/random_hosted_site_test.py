from ocfweb.main.home import hosted_site_urls


def test_hosted_site_urls_uses_primary_vhost_names():
    vhosts = {
        'lift.studentorg.berkeley.edu': {
            'username': 'lift',
            'aliases': [],
            'docroot': '/',
            'flags': [],
        },
        'bearbites.asuc.org': {
            'username': 'bearbites',
            'aliases': ['www.bearbites.asuc.org'],
            'docroot': '/',
            'flags': [],
        },
    }

    assert hosted_site_urls(vhosts) == [
        'https://bearbites.asuc.org/',
        'https://lift.studentorg.berkeley.edu/',
    ]
