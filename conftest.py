
import pytest

BASE_URL = "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="session")
def base_url():
    """Base URL of the API under test."""
    return BASE_URL


@pytest.fixture
def sample_post_payload():
    """A valid payload for creating a post."""
    return {
        "title": "Testing JSONPlaceholder API",
        "body": "This post was created by the automated test suite.",
        "userId": 1,
    }