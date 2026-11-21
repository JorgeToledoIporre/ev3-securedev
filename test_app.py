from app import app


def test_hello_route_valid():
    client = app.test_client()
    response = client.get('/hello?name=Mundo')
    assert response.status_code == 200
    assert b'Hello, Mundo!' in response.data


def test_hello_route_blocks_xss():
    client = app.test_client()
    response = client.get('/hello?name=<script>alert(1)</script>')
    assert response.status_code == 400
    assert b'<script>' not in response.data


def test_security_headers_present():
    client = app.test_client()
    response = client.get('/hello?name=Mundo')
    assert response.headers.get('X-Frame-Options') == 'DENY'
    assert response.headers.get('X-Content-Type-Options') == 'nosniff'
    assert 'Content-Security-Policy' in response.headers