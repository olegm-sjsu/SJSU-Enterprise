# Author: Oleg Mrynskyi
# CMPE 272 HW2 - GitHub Issues REST API & Webhook Service

import os
import uuid
import logging
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, Request, Response, Header, Query, Path, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.config import get_settings
from app.schemas import (
    IssueCreate, IssueUpdate, IssueResponse,
    CommentCreate, CommentResponse, EventRecord, ErrorDetail
)
from app.github_client import GitHubClient
from app.webhook import verify_webhook_signature, parse_webhook_payload
from app.database import init_db, record_webhook_event, is_duplicate_delivery, get_recent_events

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("issues-service")

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    await init_db(settings.DATABASE_PATH)
    logger.info(f"Database initialized at {settings.DATABASE_PATH}")
    yield

app = FastAPI(
    title="GitHub Issues Wrapper Service API",
    description="CMPE 272 HW2 - Contract-first REST API wrapping GitHub Issues and processing Webhook events.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)


# tag every request with a correlation id so logs can be traced end to end
@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    request.state.request_id = request_id

    logger.info(f"Incoming Request [{request_id}]: {request.method} {request.url.path}")
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


def _format_issue(raw: Dict[str, Any]) -> IssueResponse:
    labels = []
    if "labels" in raw and isinstance(raw["labels"], list):
        for lbl in raw["labels"]:
            if isinstance(lbl, dict):
                labels.append(lbl.get("name", ""))
            elif isinstance(lbl, str):
                labels.append(lbl)

    return IssueResponse(
        number=raw["number"],
        html_url=raw.get("html_url", ""),
        state=raw.get("state", "open"),
        title=raw.get("title", ""),
        body=raw.get("body"),
        labels=labels,
        created_at=raw["created_at"],
        updated_at=raw["updated_at"]
    )


def _format_comment(raw: Dict[str, Any]) -> CommentResponse:
    user_raw = raw.get("user", {})
    return CommentResponse(
        id=raw["id"],
        body=raw.get("body", ""),
        user={
            "login": user_raw.get("login", "unknown"),
            "id": user_raw.get("id", 0),
            "avatar_url": user_raw.get("avatar_url", "")
        },
        created_at=raw["created_at"],
        html_url=raw.get("html_url", "")
    )


# Observability: Structured logs; include request id and GitHub delivery id;
# a simple /healthz endpoint.
@app.get(
    "/healthz",
    tags=["System"],
    summary="Health check endpoint",
    status_code=status.HTTP_200_OK
)
async def healthz():
    return {"status": "ok", "service": "cmpe272-hw2-issues"}


# 1) POST /issues
#    Body: { title: string, body?: string, labels?: string[] }
#    Behavior: Creates a GitHub issue in the configured repo.
#    Responses:
#      201 Created → { number, html_url, state, title, body, labels, created_at, updated_at }
#      400 if invalid payload; 401 if missing/invalid token (propagate useful error info)
#    Notes:
#      - Return Location header: /issues/{number}
#      - Map external validation errors into clear messages.
@app.post(
    "/issues",
    tags=["Issues"],
    summary="Create a GitHub issue",
    status_code=status.HTTP_201_CREATED,
    response_model=IssueResponse
)
async def create_issue(
    payload: IssueCreate,
    response: Response
):
    client = GitHubClient()
    raw_issue, location = await client.create_issue(payload)
    response.headers["Location"] = location
    return _format_issue(raw_issue)


# 2) GET /issues
#    Query: state=open|closed|all (default=open), labels?, page?, per_page? (<=100)
#    Behavior: Lists issues for the repo; preserve GitHub pagination semantics.
#    Responses:
#      200 OK → [{ number, title, state, labels, ... }], plus pagination headers.
@app.get(
    "/issues",
    tags=["Issues"],
    summary="List issues for the repository",
    status_code=status.HTTP_200_OK
)
async def list_issues(
    response: Response,
    state: str = Query("open", pattern="^(open|closed|all)$", description="Filter state"),
    labels: Optional[str] = Query(None, description="Comma-separated labels"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(30, ge=1, le=100, description="Items per page (max 100)"),
    if_none_match: Optional[str] = Header(None, alias="If-None-Match", description="ETag validation header")
):
    client = GitHubClient()
    raw_issues, link_header, etag, is_not_modified = await client.list_issues(
        state=state,
        labels=labels,
        page=page,
        per_page=per_page,
        if_none_match=if_none_match
    )

    if is_not_modified:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED)

    if link_header:
        response.headers["Link"] = link_header
    if etag:
        response.headers["ETag"] = etag

    return [_format_issue(i) for i in raw_issues]


# 3) GET /issues/{number}
#    Behavior: Returns a single issue.
#    Responses: 200 OK, 404 if not found.
@app.get(
    "/issues/{number}",
    tags=["Issues"],
    summary="Get a single GitHub issue",
    status_code=status.HTTP_200_OK,
    response_model=IssueResponse
)
async def get_issue(
    number: int = Path(..., ge=1, description="Issue number")
):
    client = GitHubClient()
    raw_issue = await client.get_issue(number)
    return _format_issue(raw_issue)


# 4) PATCH /issues/{number}
#    Body: { title?, body?, state? }   # state may be "open" or "closed"
#    Behavior: Updates the issue (rename, edit body, close/open).
#    Responses: 200 OK; 400/404 on errors.
@app.patch(
    "/issues/{number}",
    tags=["Issues"],
    summary="Update a GitHub issue",
    status_code=status.HTTP_200_OK,
    response_model=IssueResponse
)
async def update_issue(
    payload: IssueUpdate,
    number: int = Path(..., ge=1, description="Issue number")
):
    client = GitHubClient()
    raw_issue = await client.update_issue(number, payload)
    return _format_issue(raw_issue)


# 5) POST /issues/{number}/comments
#    Body: { body: string }
#    Behavior: Adds a comment to the issue.
#    Responses: 201 Created → { id, body, user, created_at, html_url }
@app.post(
    "/issues/{number}/comments",
    tags=["Comments"],
    summary="Add a comment to an issue",
    status_code=status.HTTP_201_CREATED,
    response_model=CommentResponse
)
async def create_comment(
    payload: CommentCreate,
    number: int = Path(..., ge=1, description="Issue number")
):
    client = GitHubClient()
    raw_comment = await client.create_comment(number, payload)
    return _format_comment(raw_comment)


# 6) POST /webhook
#    Behavior:
#      - Verify HMAC SHA-256 signature using WEBHOOK_SECRET.
#      - Accept events: "issues", "issue_comment" (and "ping").
#      - On valid signature + known event: persist event to a local store (file/SQLite/in-memory ok), log summary.
#      - Respond 2xx quickly (ack), never block on long work. Use retry-safe handling.
#    Responses:
#      204 No Content on success; 401 if signature invalid; 400 for unknown event/action.
@app.post(
    "/webhook",
    tags=["Webhooks"],
    summary="GitHub Webhook receiver endpoint",
    status_code=status.HTTP_204_NO_CONTENT
)
async def handle_webhook(
    request: Request,
    x_hub_signature_256: Optional[str] = Header(None, alias="X-Hub-Signature-256"),
    x_github_event: Optional[str] = Header(None, alias="X-GitHub-Event"),
    x_github_delivery: Optional[str] = Header(None, alias="X-GitHub-Delivery")
):
    settings = get_settings()
    raw_body = await request.body()

    if not verify_webhook_signature(raw_body, x_hub_signature_256, settings.WEBHOOK_SECRET):
        logger.warning("Webhook HMAC signature verification failed")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-Hub-Signature-256 signature"
        )

    event_type = x_github_event or "unknown"
    if event_type not in ("issues", "issue_comment", "ping"):
        logger.warning(f"Rejected unsupported webhook event type: {event_type}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported event type: {event_type}"
        )

    delivery_id = x_github_delivery or str(uuid.uuid4())

    # already seen this delivery id -> just ack, don't reprocess
    if await is_duplicate_delivery(delivery_id, settings.DATABASE_PATH):
        logger.info(f"Duplicate webhook delivery ACK: {delivery_id}")
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    action, issue_number, _ = parse_webhook_payload(event_type, raw_body)
    await record_webhook_event(
        delivery_id=delivery_id,
        event=event_type,
        action=action,
        issue_number=issue_number,
        payload=raw_body.decode("utf-8", errors="ignore"),
        db_path=settings.DATABASE_PATH
    )

    logger.info(f"Processed webhook event '{event_type}' ({action}) for issue #{issue_number}")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# 7) GET /events (optional but recommended)
#    Behavior: Returns the last N processed webhook deliveries for debugging.
#    Response: 200 OK → array of { id, event, action, issue_number, timestamp }
@app.get(
    "/events",
    tags=["Webhooks"],
    summary="List recent processed webhook delivery events",
    status_code=status.HTTP_200_OK,
    response_model=List[EventRecord]
)
async def list_events(
    limit: int = Query(50, ge=1, le=100, description="Max delivery events to return")
):
    settings = get_settings()
    return await get_recent_events(limit, settings.DATABASE_PATH)


# mounted last so it only catches paths the routes above didn't claim
STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "static")
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
