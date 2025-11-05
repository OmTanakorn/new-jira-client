"""FastAPI dependencies and utilities."""
from typing import Optional
from fastapi import Depends, HTTPException, status
from app.auth.middleware import get_current_user
from app.utils.jira_client import JiraClient


async def get_jira_client(
    current_user: dict = Depends(get_current_user)
) -> JiraClient:
    """Get Jira client with user's access token.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Configured JiraClient instance
        
    Raises:
        HTTPException: If access token is not available
    """
    access_token = current_user.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No access token available"
        )
    
    return JiraClient(access_token=access_token)
