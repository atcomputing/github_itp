"""
Pytest configuration and shared fixtures for In The Picture tests.

This file is automatically loaded by pytest and provides:
- Shared fixtures used across multiple test files
- Test environment setup and teardown
- Temporary directories for isolated test execution
"""

import pytest
import os
import sys

# Add app directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))


@pytest.fixture
def test_upload_dir(tmp_path):
    """
    Create a temporary upload directory for tests.

    This ensures tests don't pollute the real uploads directory.
    Each test gets its own isolated temporary directory.
    """
    upload_dir = tmp_path / "test_uploads"
    upload_dir.mkdir()
    return str(upload_dir)


@pytest.fixture
def mock_image_file():
    """
    Create a mock image file for upload testing.

    Returns a file-like object that simulates an uploaded image.
    """
    from io import BytesIO

    # Create a minimal valid PNG file (1x1 pixel)
    png_data = (
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
        b'\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\x00\x01'
        b'\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
    )

    return BytesIO(png_data)
