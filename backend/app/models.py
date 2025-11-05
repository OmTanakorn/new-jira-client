"""Pydantic models for request/response validation."""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class JiraSearchRequest(BaseModel):
    """Request model for Jira issue search."""
    jql: str = Field(..., description="JQL query string")
    fields: Optional[List[str]] = Field(
        default=None,
        description="List of fields to return"
    )
    max_results: int = Field(default=50, le=100, description="Maximum results to return")
    start_at: int = Field(default=0, description="Starting index for pagination")


class IssueTransitionRequest(BaseModel):
    """Request model for issue transition."""
    transition_id: str = Field(..., description="ID of the transition to execute")


class IssueUpdateRequest(BaseModel):
    """Request model for issue field updates."""
    fields: Dict[str, Any] = Field(..., description="Fields to update")


class JiraIssue(BaseModel):
    """Response model for Jira issue."""
    key: str
    summary: str
    status: str
    assignee: Optional[str] = None
    priority: Optional[str] = None
    issue_type: str
    description: Optional[str] = None


class JiraProject(BaseModel):
    """Response model for Jira project."""
    id: str
    key: str
    name: str


class OAuthCallbackRequest(BaseModel):
    """Request model for OAuth callback."""
    code: str = Field(..., description="Authorization code from OAuth provider")
    state: Optional[str] = Field(None, description="State parameter for CSRF protection")


class UserInfo(BaseModel):
    """Response model for user information."""
    account_id: str
    email: Optional[str] = None
    display_name: str
    avatar_url: Optional[str] = None


class WebhookEvent(BaseModel):
    """Base model for Jira webhook events."""
    webhook_event: str
    issue_event_type_name: Optional[str] = None
    issue: Optional[Dict[str, Any]] = None
    changelog: Optional[Dict[str, Any]] = None
