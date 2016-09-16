def tests_robots_dot_txt(client):
    resp = client.get('/robots.txt')
    assert resp.status_code == 200
    assert resp.get('Content-Type') == 'text/plain'

    lines = resp.content.splitlines()
    assert 2 <= len(lines) <= 50
    assert b'Disallow: /test/' in lines
