from typing import Any, Dict, Generator
import pytest
from flask import Flask
from flask.testing import FlaskClient
from werkzeug.datastructures import Headers

# Assuming your app is created in a module named 'app'
from app import create_app
from app.extensions import db

@pytest.fixture
def app() -> Generator[Flask]:
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()

@pytest.fixture
def auth_headers(client: FlaskClient) -> Headers:
    # Register a test user
    register_data = {
        "username": "testuser",
        "name": "Test User",
        "email": "test@example.com",
        "password": "TestPass123"
    }
    client.post('/api/register', json=register_data)
    
    # Login to get token
    login_data = {
        "email": "test@example.com",
        "password": "TestPass123"
    }
    response = client.post('/api/login', json=login_data)
    token = response.json['access_token']
    headers = Headers()
    headers.add('Authorization', f'Bearer {token}')
    return headers

@pytest.fixture
def test_movie(client: FlaskClient, auth_headers: Headers) -> Dict[Any, Any] | None:
    movie_data: Dict[str, int| str] = {
        "title": "Inception",
        "year": 2010,
        "genre": "Sci-Fi",
        "duration": 148
    }
    response = client.post(
        '/api/movies', 
        json=movie_data, 
        headers=auth_headers
    )
    if response.status_code == 308:
        redirect_location = response.headers.get('Location')
        response = client.post(redirect_location, json=movie_data, headers=auth_headers)
    assert response.status_code == 201
    
    return response.json
