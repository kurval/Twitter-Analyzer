import pytest
from app import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_welcome_text(app, client):
    res = client.get('/')
    assert res.status_code == 200
    expected = 'Welcome to Twitter Analyzer!'
    exp = res.get_data(as_text=True)
    assert expected in exp