import pytest
import os


@pytest.fixture
def url():
    """A test url """
    url = os.environ.get('TEST_URL', 'http://localhost:5000')
    return url