"""FastAPI main application with routes."""
import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from dotenv import load_dotenv

from app.models import (
    JiraSearchRequest,
    IssueTransitionRequest,
    IssueUpdateRequest,
    OAuthCallbackRequest,
    WebhookEvent,
)
from app.auth.oauth import JiraOAuth
from app.auth.middleware import get_current_user, create_access_token
from app.deps import get_jira_client
from app.utils.jira_client import JiraClient
from app.webhooks.validators import validate_webhook_payload
from app.webhooks.handlers import process_webhook_event
from app import jira_proxy


# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if os.getenv("DEBUG", "false").lower() == "true" else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    # Startup
    logger.info("Starting New Jira Client API")
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    logger.info(f"Frontend URL: {frontend_url}")
    logger.info(f"Debug mode: {os.getenv('DEBUG', 'false')}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down New Jira Client API")


# Initialize FastAPI app
app = FastAPI(
    title="New Jira Client API",
    description="FastAPI proxy server for New Jira Client",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OAuth handler
oauth = JiraOAuth()


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "New Jira Client API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Authentication endpoints
@app.get("/auth/login")
async def login():
    """Initiate Jira OAuth flow."""
    auth_url = oauth.get_authorization_url()
    return {"authorization_url": auth_url}


@app.post("/auth/callback")
async def oauth_callback(callback_request: OAuthCallbackRequest):
    """Handle OAuth callback and exchange code for token.
    
    Args:
        callback_request: OAuth callback parameters
        
    Returns:
        Access token and user information
    """
    try:
        # Exchange code for token
        token_response = await oauth.exchange_code_for_token(callback_request.code)
        access_token = token_response.get("access_token")
        refresh_token = token_response.get("refresh_token")
        
        # Get user info
        user_info = await oauth.get_user_info(access_token)
        
        # Create JWT token with user info and Jira tokens
        jwt_payload = {
            "account_id": user_info.get("account_id"),
            "email": user_info.get("email"),
            "name": user_info.get("name"),
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
        jwt_token = create_access_token(jwt_payload)
        
        return {
            "access_token": jwt_token,
            "token_type": "bearer",
            "user": {
                "account_id": user_info.get("account_id"),
                "email": user_info.get("email"),
                "name": user_info.get("name"),
            }
        }
    except Exception as e:
        logger.error(f"OAuth callback error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Authentication failed: {str(e)}"
        )


@app.get("/auth/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current authenticated user information.
    
    Args:
        current_user: Current user from JWT token
        
    Returns:
        User information
    """
    return {
        "account_id": current_user.get("account_id"),
        "email": current_user.get("email"),
        "name": current_user.get("name"),
    }


@app.post("/auth/logout")
async def logout():
    """Logout endpoint (client-side token removal)."""
    return {"message": "Logged out successfully"}


# Jira proxy endpoints
@app.get("/api/projects")
async def get_projects(jira_client: JiraClient = Depends(get_jira_client)):
    """Get list of accessible Jira projects.
    
    Args:
        jira_client: Authenticated Jira client
        
    Returns:
        List of projects
    """
    try:
        projects = await jira_proxy.get_projects_proxy(jira_client)
        return {"projects": projects}
    except Exception as e:
        logger.error(f"Error fetching projects: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch projects: {str(e)}"
        )


@app.post("/api/search")
async def search_issues(
    search_request: JiraSearchRequest,
    jira_client: JiraClient = Depends(get_jira_client)
):
    """Search for Jira issues using JQL.
    
    Args:
        search_request: Search parameters
        jira_client: Authenticated Jira client
        
    Returns:
        Search results
    """
    try:
        results = await jira_proxy.search_issues_proxy(search_request, jira_client)
        return results
    except Exception as e:
        logger.error(f"Error searching issues: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search issues: {str(e)}"
        )


@app.get("/api/issues/{issue_key}")
async def get_issue(
    issue_key: str,
    jira_client: JiraClient = Depends(get_jira_client)
):
    """Get details for a specific issue.
    
    Args:
        issue_key: Issue key (e.g., 'PROJ-123')
        jira_client: Authenticated Jira client
        
    Returns:
        Issue details
    """
    try:
        issue = await jira_proxy.get_issue_proxy(issue_key, jira_client)
        return issue
    except Exception as e:
        logger.error(f"Error fetching issue {issue_key}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch issue: {str(e)}"
        )


@app.put("/api/issues/{issue_key}/transition")
async def transition_issue(
    issue_key: str,
    transition_request: IssueTransitionRequest,
    jira_client: JiraClient = Depends(get_jira_client)
):
    """Transition an issue to a new status.
    
    Args:
        issue_key: Issue key (e.g., 'PROJ-123')
        transition_request: Transition parameters
        jira_client: Authenticated Jira client
        
    Returns:
        Transition result
    """
    try:
        result = await jira_proxy.transition_issue_proxy(
            issue_key, transition_request, jira_client
        )
        return result
    except Exception as e:
        logger.error(f"Error transitioning issue {issue_key}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to transition issue: {str(e)}"
        )


@app.put("/api/issues/{issue_key}")
async def update_issue(
    issue_key: str,
    update_request: IssueUpdateRequest,
    jira_client: JiraClient = Depends(get_jira_client)
):
    """Update issue fields.
    
    Args:
        issue_key: Issue key (e.g., 'PROJ-123')
        update_request: Update parameters
        jira_client: Authenticated Jira client
        
    Returns:
        Update result
    """
    try:
        result = await jira_proxy.update_issue_proxy(
            issue_key, update_request, jira_client
        )
        return result
    except Exception as e:
        logger.error(f"Error updating issue {issue_key}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update issue: {str(e)}"
        )


# Webhook endpoint
@app.post("/webhooks/jira")
async def jira_webhook(event: WebhookEvent):
    """Handle Jira webhook events.
    
    Args:
        event: Webhook event data
        
    Returns:
        Acknowledgment response
    """
    try:
        payload = event.dict()
        
        # Validate webhook payload
        if not validate_webhook_payload(payload):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid webhook payload"
            )
        
        # Process webhook event asynchronously
        await process_webhook_event(payload)
        
        return {"status": "received"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process webhook: {str(e)}"
        )
