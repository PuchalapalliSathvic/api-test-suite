"""Tests for the /posts endpoint (GET, POST, PUT, DELETE)."""

import requests

POST_SCHEMA_KEYS = {"userId", "id", "title", "body"}


class TestGetPosts:
    """GET /posts — read operations."""

    def test_get_all_posts_returns_200_and_full_list(self, base_url):
        response = requests.get(f"{base_url}/posts")
        assert response.status_code == 200
        body = response.json()
        assert isinstance(body, list)
        assert len(body) == 100

    def test_get_single_post_returns_correct_structure(self, base_url):
        response = requests.get(f"{base_url}/posts/1")
        assert response.status_code == 200
        body = response.json()
        assert set(body.keys()) == POST_SCHEMA_KEYS
        assert body["id"] == 1

    def test_get_nonexistent_post_returns_404(self, base_url):
        response = requests.get(f"{base_url}/posts/9999")
        assert response.status_code == 404


class TestCreatePost:
    """POST /posts — create operations.

    Note: JSONPlaceholder simulates writes. It returns a realistic
    response (201 + echoed body + new id) but does not persist data,
    so assertions target the response itself.
    """

    def test_create_post_returns_201_and_echoes_payload(
        self, base_url, sample_post_payload
    ):
        response = requests.post(f"{base_url}/posts", json=sample_post_payload)
        assert response.status_code == 201
        body = response.json()
        assert body["title"] == sample_post_payload["title"]
        assert body["body"] == sample_post_payload["body"]
        assert body["userId"] == sample_post_payload["userId"]

    def test_create_post_assigns_new_id(self, base_url, sample_post_payload):
        response = requests.post(f"{base_url}/posts", json=sample_post_payload)
        assert response.status_code == 201
        assert response.json()["id"] == 101


class TestUpdatePost:
    """PUT /posts/{id} — update operations."""

    def test_update_post_returns_200_with_updated_fields(self, base_url):
        payload = {"id": 1, "title": "Updated title", "body": "Updated body", "userId": 1}
        response = requests.put(f"{base_url}/posts/1", json=payload)
        assert response.status_code == 200
        body = response.json()
        assert body["title"] == "Updated title"
        assert body["id"] == 1


class TestDeletePost:
    """DELETE /posts/{id} — delete operations."""

    def test_delete_post_returns_200(self, base_url):
        response = requests.delete(f"{base_url}/posts/1")
        assert response.status_code == 200
