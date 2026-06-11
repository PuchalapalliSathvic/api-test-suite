"""Tests for the /users endpoint (GET) — focuses on nested data structure."""

import requests

USER_TOP_LEVEL_KEYS = {
    "id", "name", "username", "email",
    "address", "phone", "website", "company",
}


class TestGetUsers:
    """GET /users — read operations and schema validation."""

    def test_get_all_users_returns_200_and_ten_users(self, base_url):
        response = requests.get(f"{base_url}/users")
        assert response.status_code == 200
        body = response.json()
        assert isinstance(body, list)
        assert len(body) == 10

    def test_get_single_user_has_expected_schema(self, base_url):
        response = requests.get(f"{base_url}/users/1")
        assert response.status_code == 200
        assert set(response.json().keys()) == USER_TOP_LEVEL_KEYS

    def test_user_nested_address_structure(self, base_url):
        response = requests.get(f"{base_url}/users/1")
        address = response.json()["address"]
        assert {"street", "suite", "city", "zipcode", "geo"} <= set(address.keys())
        float(address["geo"]["lat"])
        float(address["geo"]["lng"])

    def test_get_nonexistent_user_returns_404(self, base_url):
        response = requests.get(f"{base_url}/users/9999")
        assert response.status_code == 404
