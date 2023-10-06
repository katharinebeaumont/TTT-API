import os
import tempfile

import pytest


# Needs to combine response writer with graph helper methods

@pytest.fixture
def app():

    app = create_app({
        'TESTING': True
    })
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'
