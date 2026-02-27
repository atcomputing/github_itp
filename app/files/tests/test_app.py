"""
Test suite for In The Picture application.
Tests basic functionality of routes and image handling.

These tests are designed to be "turn key" - students run them without
modifying test code. Focus is on understanding CI/CD, not writing tests.
"""

import pytest
import os
import sys

# Add app directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

from app import app as flask_app


@pytest.fixture
def app():
    """Create Flask application for testing."""
    flask_app.config['TESTING'] = True
    flask_app.config['UPLOAD_FOLDER'] = 'test_uploads'
    return flask_app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


# Test 1: Home page loads successfully
def test_home_page(client):
    """Test that home page returns 200 OK."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'IN THE PICTURE' in response.data


# Test 2: Preview route exists
def test_preview_route(client):
    """Test that preview route loads (even without image)."""
    response = client.get('/preview/test.jpg')
    assert response.status_code == 200


# Test 3: Upload route accepts GET requests
def test_upload_get(client):
    """Test that upload page loads with GET request."""
    response = client.get('/upload')
    assert response.status_code == 200


# Test 4: Static files route works
def test_static_route(client):
    """Test that static files can be accessed."""
    # This test will FAIL initially - FIX REQUIRED
    response = client.get('/static/bootstrap.min.css')
    # UNCOMMENT THE LINE BELOW TO FIX THE TEST:
    # assert response.status_code == 200
    assert response.status_code == 404  # This will fail! Change to 200 to fix


# Test 5: Invalid upload is rejected
def test_invalid_upload(client):
    """Test that empty file upload is handled correctly."""
    data = {'file': (None, '')}
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    # Should redirect or show error (not crash)
    assert response.status_code in [200, 302]
