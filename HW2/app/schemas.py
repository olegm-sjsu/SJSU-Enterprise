# Author: Oleg Mrynskyi
# CMPE 272 HW2 - GitHub Issues REST API & Webhook Service

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

# --- issues ---

class IssueCreate(BaseModel):
    """POST /issues body."""
    title: str = Field(..., min_length=1, description="Issue title")
    body: Optional[str] = Field(default=None, description="Issue body/description")
    labels: Optional[List[str]] = Field(default=None, description="List of labels")


class IssueUpdate(BaseModel):
    """PATCH /issues/{number} body."""
    title: Optional[str] = Field(default=None, description="Updated issue title")
    body: Optional[str] = Field(default=None, description="Updated issue body")
    state: Optional[str] = Field(default=None, pattern="^(open|closed)$", description="Target state: open or closed")


class IssueResponse(BaseModel):
    number: int
    html_url: str
    state: str
    title: str
    body: Optional[str] = None
    labels: List[str] = []
    created_at: datetime
    updated_at: datetime


# --- comments ---

class CommentCreate(BaseModel):
    """POST /issues/{number}/comments body."""
    body: str = Field(..., min_length=1, description="Comment text body")


class CommentUser(BaseModel):
    login: str
    id: int
    avatar_url: str


class CommentResponse(BaseModel):
    id: int
    body: str
    user: CommentUser
    created_at: datetime
    html_url: str


# --- webhook / event log (GET /events) ---

class EventRecord(BaseModel):
    id: int
    delivery_id: str
    event: str
    action: Optional[str] = None
    issue_number: Optional[int] = None
    timestamp: datetime


# --- error response ---

class ErrorDetail(BaseModel):
    status_code: int
    message: str
    details: Optional[dict] = None
    request_id: Optional[str] = None
