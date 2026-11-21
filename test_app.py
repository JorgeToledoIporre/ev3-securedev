from app import app

def test_hello_route():
    client = app.test_client()
    response = client.get('/hello?name=Mundo')
    assert response.status_code == 200
    assert b'Hello, Mundo!' in response.data