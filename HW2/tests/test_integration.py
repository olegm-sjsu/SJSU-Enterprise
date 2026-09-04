# Author: Oleg Mrynskyi

import os
import hmac
import hashlib
import json
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import init_db

SECRET = "integration_secret_key"
TEST_DB = "test_events.db"

@pytest_asyncio.fixture(autouse=True)
async def setup_test_environment(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "mock_integration_pat")
    monkeypatch.setenv("GITHUB_OWNER", "test-owner")
    monkeypatch.setenv("GITHUB_REPO", "test-repo")
    monkeypatch.setenv("WEBHOOK_SECRET", SECRET)
    monkeypatch.setenv("PORT", "8000")
    monkeypatch.setenv("DATABASE_PATH", TEST_DB)
    
    # Initialize DB for tests
    await init_db(TEST_DB)
    yield
    # Clean up test db file after test
    if os.path.exists(TEST_DB):
        try:
            os.remove(TEST_DB)
        except OSError:
            pass


@pytest.mark.asyncio
async def test_full_issue_crud_lifecycle_integration(httpx_mock):
    httpx_mock.add_response(
        method="POST",
        url="https://api.github.com/repos/test-owner/test-repo/issues",
        status_code=201,
        json={
            "number": 10,
            "html_url": "https://github.com/test-owner/test-repo/issues/10",
            "state": "open",
            "title": "Integration Test Issue",
            "body": "Integration Body",
            "labels": [{"name": "integration"}],
            "created_at": "2026-09-01T12:00:00Z",
            "updated_at": "2026-09-01T12:00:00Z"
        }
    )

    httpx_mock.add_response(
        method="GET",
        url="https://api.github.com/repos/test-owner/test-repo/issues/10",
        status_code=200,
        json={
            "number": 10,
            "html_url": "https://github.com/test-owner/test-repo/issues/10",
            "state": "open",
            "title": "Integration Test Issue",
            "body": "Integration Body",
            "labels": [{"name": "integration"}],
            "created_at": "2026-09-01T12:00:00Z",
            "updated_at": "2026-09-01T12:00:00Z"
        }
    )

    httpx_mock.add_response(
        method="PATCH",
        url="https://api.github.com/repos/test-owner/test-repo/issues/10",
        status_code=200,
        json={
            "number": 10,
            "html_url": "https://github.com/test-owner/test-repo/issues/10",
            "state": "closed",
            "title": "Updated Integration Issue",
            "body": "Updated Body",
            "labels": [{"name": "integration"}],
            "created_at": "2026-09-01T12:00:00Z",
            "updated_at": "2026-09-01T12:05:00Z"
        }
    )

    httpx_mock.add_response(
        method="POST",
        url="https://api.github.com/repos/test-owner/test-repo/issues/10/comments",
        status_code=201,
        json={
            "id": 501,
            "body": "Integration Comment",
            "user": {"login": "tester", "id": 1, "avatar_url": ""},
            "created_at": "2026-09-01T12:10:00Z",
            "html_url": "https://github.com/test-owner/test-repo/issues/10#issuecomment-501"
        }
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        # 1. Create Issue
        create_res = await ac.post("/issues", json={"title": "Integration Test Issue", "body": "Integration Body"})
        assert create_res.status_code == 201
        assert create_res.headers["Location"] == "/issues/10"
        assert create_res.json()["number"] == 10

        # 2. Get Issue
        get_res = await ac.get("/issues/10")
        assert get_res.status_code == 200
        assert get_res.json()["title"] == "Integration Test Issue"

        # 3. Patch Issue
        patch_res = await ac.patch("/issues/10", json={"title": "Updated Integration Issue", "state": "closed"})
        assert patch_res.status_code == 200
        assert patch_res.json()["state"] == "closed"

        # 4. Add Comment
        comment_res = await ac.post("/issues/10/comments", json={"body": "Integration Comment"})
        assert comment_res.status_code == 201
        assert comment_res.json()["id"] == 501


@pytest.mark.asyncio
async def test_webhook_delivery_and_events_retrieval():
    payload = json.dumps({"action": "opened", "issue": {"number": 100}}).encode("utf-8")
    computed_sig = f"sha256={hmac.new(SECRET.encode('utf-8'), payload, hashlib.sha256).hexdigest()}"

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        # Send Webhook
        webhook_res = await ac.post(
            "/webhook",
            headers={
                "X-GitHub-Event": "issues",
                "X-GitHub-Delivery": "delivery-unique-1234",
                "X-Hub-Signature-256": computed_sig
            },
            content=payload
        )
        assert webhook_res.status_code == 204

        # Verify duplicate delivery returns 204
        dup_res = await ac.post(
            "/webhook",
            headers={
                "X-GitHub-Event": "issues",
                "X-GitHub-Delivery": "delivery-unique-1234",
                "X-Hub-Signature-256": computed_sig
            },
            content=payload
        )
        assert dup_res.status_code == 204

        # Retrieve Events
        events_res = await ac.get("/events")
        assert events_res.status_code == 200
        events = events_res.json()
        assert len(events) >= 1
        assert events[0]["delivery_id"] == "delivery-unique-1234"
