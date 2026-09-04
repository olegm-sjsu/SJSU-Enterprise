# Author: Oleg Mrynskyi

import pytest
import pytest_asyncio
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


def test_healthz():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "cmpe272-hw2-issues"}


def test_create_issue_missing_title():
    """POST /issues without title must return 422 validation error."""
    response = client.post("/issues", json={"body": "Missing title!"})
    assert response.status_code == 422


def test_patch_issue_invalid_state():
    """PATCH /issues/{number} with invalid state must fail validation."""
    response = client.patch("/issues/1", json={"state": "invalid_state"})
    assert response.status_code == 422


@patch("app.github_client.GitHubClient.get_issue", new_callable=AsyncMock)
def test_get_issue_success(mock_get_issue):
    mock_get_issue.return_value = {
        "number": 1,
        "html_url": "https://github.com/unit-owner/unit-repo/issues/1",
        "state": "open",
        "title": "Test Issue",
        "body": "Test Body",
        "labels": [{"name": "bug"}],
        "created_at": "2026-09-01T10:00:00Z",
        "updated_at": "2026-09-01T10:00:00Z"
    }

    response = client.get("/issues/1")
    assert response.status_code == 200
    data = response.json()
    assert data["number"] == 1
    assert data["title"] == "Test Issue"
    assert data["labels"] == ["bug"]


@patch("app.github_client.GitHubClient.create_issue", new_callable=AsyncMock)
def test_create_issue_success(mock_create_issue):
    mock_create_issue.return_value = (
        {
            "number": 42,
            "html_url": "https://github.com/unit-owner/unit-repo/issues/42",
            "state": "open",
            "title": "New Bug",
            "body": "Bug description",
            "labels": [],
            "created_at": "2026-09-01T10:00:00Z",
            "updated_at": "2026-09-01T10:00:00Z"
        },
        "/issues/42"
    )

    response = client.post("/issues", json={"title": "New Bug", "body": "Bug description"})
    assert response.status_code == 201
    assert response.headers["Location"] == "/issues/42"
    assert response.json()["number"] == 42
