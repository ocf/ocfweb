import requests


def tests_robots_dot_txt(running_server):
    resp = requests.get(running_server + '/robots.txt')
    assert resp.status_code == 200
    assert resp.headers['Content-Type'] == 'text/plain'

    lines = resp.text.splitlines()
    assert 2 <= len(lines) <= 50
    assert 'Disallow: /test/' in lines
