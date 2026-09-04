# Author: Oleg Mrynskyi

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_unit_environment(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "mock_unit_token")
    monkeypatch.setenv("GITHUB_OWNER", "unit-owner")
    monkeypatch.setenv("GITHUB_REPO", "unit-repo")
    monkeypatch.setenv("WEBHOOK_SECRET", "unit_secret")
    monkeypatch.setenv("PORT", "8000")
    yield


@patch("app.github_client.GitHubClient.list_issues", new_callable=AsyncMock)
def test_list_issues_pagination_headers(mock_list_issues):
    mock_list_issues.return_value = (
        [
            {
                "number": 1,
                "html_url": "https://github.com/owner/repo/issues/1",
                "state": "open",
                "title": "Issue 1",
                "body": "Body 1",
                "labels": [],
                "created_at": "2026-09-01T10:00:00Z",
                "updated_at": "2026-09-01T10:00:00Z"
            }
        ],
        '<https://api.github.com/repos/owner/repo/issues?page=2>; rel="next"',
        'W/"123456789"',
        False
    )

    response = client.get("/issues?page=1&per_page=10")
    assert response.status_code == 200
    assert response.headers["Link"] == '<https://api.github.com/repos/owner/repo/issues?page=2>; rel="next"'
    assert response.headers["ETag"] == 'W/"123456789"'
    assert len(response.json()) == 1


@patch("app.github_client.GitHubClient.list_issues", new_callable=AsyncMock)
def test_conditional_get_etag_304(mock_list_issues):
    mock_list_issues.return_value = ([], None, 'W/"123456789"', True)

    response = client.get("/issues", headers={"If-None-Match": 'W/"123456789"'})
    assert response.status_code == 304


def test_per_page_max_limit():
    response = client.get("/issues?per_page=150")
    assert response.status_code == 422
