# Author: Oleg Mrynskyi
# CMPE 272 HW2 - GitHub Issues REST API & Webhook Service

import httpx
from typing import Dict, Any, List, Optional, Tuple
from fastapi import HTTPException, status
from app.config import Settings, get_settings
from app.schemas import IssueCreate, IssueUpdate, CommentCreate

class GitHubClient:
    # thin async wrapper around the GitHub REST API for issues + comments

    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or get_settings()
        
        missing = []
        if not self.settings.GITHUB_TOKEN:
            missing.append("GITHUB_TOKEN")
        if not self.settings.GITHUB_OWNER:
            missing.append("GITHUB_OWNER")
        if not self.settings.GITHUB_REPO:
            missing.append("GITHUB_REPO")
            
        if missing:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED if "GITHUB_TOKEN" in missing else status.HTTP_400_BAD_REQUEST,
                detail=f"Missing configuration in .env file: {', '.join(missing)}"
            )

        self.base_url = f"https://api.github.com/repos/{self.settings.GITHUB_OWNER}/{self.settings.GITHUB_REPO}"
        token_clean = self.settings.GITHUB_TOKEN.strip()
        self.headers = {
            "Authorization": f"Bearer {token_clean}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "CMPE272-Issues-GW/1.0"
        }

    # maps GitHub's error responses onto our own HTTPExceptions
    def _handle_error_response(self, response: httpx.Response) -> None:
        status_code = response.status_code
        if status_code < 400:
            return

        try:
            error_body = response.json()
        except Exception:
            error_body = {"message": response.text}

        msg = error_body.get("message", "")

        if status_code == 401:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"GitHub Authentication Failed: {msg or 'Invalid token'}"
            )
        elif status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Resource not found on GitHub: {msg or 'Not Found'}"
            )
        elif status_code == 429 or (status_code == 403 and response.headers.get("X-RateLimit-Remaining") == "0"):
            retry_after = response.headers.get("Retry-After") or response.headers.get("X-RateLimit-Reset", "60")
            headers = {"Retry-After": str(retry_after)}
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"GitHub API Rate Limit Exceeded: {msg or 'Rate limited'}",
                headers=headers
            )
        elif status_code == 403:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"GitHub Permission Error: {msg}. Please ensure your Fine-Grained PAT has 'Issues: Read and Write' permissions for repository '{self.settings.GITHUB_REPO}'."
            )
        elif status_code in (400, 422):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"GitHub Validation Error: {msg or 'Invalid payload'}"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"GitHub Upstream Error ({status_code}): {msg or 'Server error'}"
            )

    async def create_issue(self, payload: IssueCreate) -> Tuple[Dict[str, Any], str]:
        url = f"{self.base_url}/issues"
        body = {"title": payload.title}
        if payload.body is not None:
            body["body"] = payload.body
        if payload.labels is not None:
            body["labels"] = payload.labels

        async with httpx.AsyncClient() as client:
            res = await client.post(url, json=body, headers=self.headers, timeout=10.0)
            self._handle_error_response(res)
            data = res.json()
            number = data.get("number")
            location = f"/issues/{number}"
            return data, location

    async def list_issues(
        self,
        state: str = "open",
        labels: Optional[str] = None,
        page: int = 1,
        per_page: int = 30,
        if_none_match: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], Optional[str], Optional[str], bool]:
        url = f"{self.base_url}/issues"
        params = {"state": state, "page": page, "per_page": min(per_page, 100)}
        if labels:
            params["labels"] = labels

        request_headers = dict(self.headers)
        if if_none_match:
            request_headers["If-None-Match"] = if_none_match

        async with httpx.AsyncClient() as client:
            res = await client.get(url, params=params, headers=request_headers, timeout=10.0)

            if res.status_code == 304:
                return [], None, if_none_match, True

            self._handle_error_response(res)

            issues = res.json()
            link_header = res.headers.get("Link")
            etag = res.headers.get("ETag")
            return issues, link_header, etag, False

    async def get_issue(self, issue_number: int) -> Dict[str, Any]:
        url = f"{self.base_url}/issues/{issue_number}"
        async with httpx.AsyncClient() as client:
            res = await client.get(url, headers=self.headers, timeout=10.0)
            self._handle_error_response(res)
            return res.json()

    async def update_issue(self, issue_number: int, payload: IssueUpdate) -> Dict[str, Any]:
        url = f"{self.base_url}/issues/{issue_number}"
        body = {}
        if payload.title is not None:
            body["title"] = payload.title
        if payload.body is not None:
            body["body"] = payload.body
        if payload.state is not None:
            body["state"] = payload.state

        async with httpx.AsyncClient() as client:
            res = await client.patch(url, json=body, headers=self.headers, timeout=10.0)
            self._handle_error_response(res)
            return res.json()

    async def create_comment(self, issue_number: int, payload: CommentCreate) -> Dict[str, Any]:
        url = f"{self.base_url}/issues/{issue_number}/comments"
        body = {"body": payload.body}

        async with httpx.AsyncClient() as client:
            res = await client.post(url, json=body, headers=self.headers, timeout=10.0)
            self._handle_error_response(res)
            return res.json()
