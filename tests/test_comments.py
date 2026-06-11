"""Tests for the /comments endpoint (GET) — includes query-param filtering."""

import requests

COMMENT_SCHEMA_KEYS = {"postId", "id", "name", "email", "body"}


class TestGetComments:
    """GET /comments — read operations and filtering."""

    def test_get_all_comments_returns_200(self, base_url):
        response = requests.get(f"{base_url}/comments")
        assert response.status_code == 200
        assert len(response.json()) == 500

    def test_get_single_comment_structure(self, base_url):
        response = requests.get(f"{base_url}/comments/1")
        assert response.status_code == 200
        assert set(response.json().keys()) == COMMENT_SCHEMA_KEYS

    def test_filter_comments_by_post_id(self, base_url):
        response = requests.get(f"{base_url}/comments", params={"postId": 1})
        assert response.status_code == 200
        comments = response.json()
        assert len(comments) > 0
        assert all(comment["postId"] == 1 for comment in comments)

    def test_filter_with_invalid_post_id_returns_empty_list(self, base_url):
        response = requests.get(f"{base_url}/comments", params={"postId": 9999})
        assert response.status_code == 200
        assert response.json() == []
