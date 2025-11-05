"""Jira OAuth 2.0 3LO (3-Legged OAuth) implementation."""
import os
import httpx
from typing import Dict, Any, Optional
from urllib.parse import urlencode


class JiraOAuth:
    """Handle Jira OAuth 2.0 3LO flow."""
    
    def __init__(self):
        """Initialize OAuth handler with configuration from environment."""
        self.client_id = os.getenv("JIRA_CLIENT_ID", "")
        self.client_secret = os.getenv("JIRA_CLIENT_SECRET", "")
        self.redirect_uri = os.getenv("JIRA_REDIRECT_URI", "")
        self.base_url = os.getenv("JIRA_BASE_URL", "")
        
        # OAuth endpoints
        self.auth_url = "https://auth.atlassian.com/authorize"
        self.token_url = "https://auth.atlassian.com/oauth/token"
        
    def get_authorization_url(self, state: Optional[str] = None) -> str:
        """Generate OAuth authorization URL.
        
        Args:
            state: Optional state parameter for CSRF protection
            
        Returns:
            Authorization URL to redirect user to
        """
        params = {
            "audience": "api.atlassian.com",
            "client_id": self.client_id,
            "scope": "read:jira-work write:jira-work offline_access",
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "prompt": "consent",
        }
        if state:
            params["state"] = state
            
        return f"{self.auth_url}?{urlencode(params)}"
    
    async def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token.
        
        Args:
            code: Authorization code from OAuth callback
            
        Returns:
            Token response containing access_token, refresh_token, etc.
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.token_url,
                json={
                    "grant_type": "authorization_code",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code,
                    "redirect_uri": self.redirect_uri,
                }
            )
            response.raise_for_status()
            return response.json()
    
    async def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh access token using refresh token.
        
        Args:
            refresh_token: Refresh token from previous authentication
            
        Returns:
            New token response
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.token_url,
                json={
                    "grant_type": "refresh_token",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "refresh_token": refresh_token,
                }
            )
            response.raise_for_status()
            return response.json()
    
    async def get_accessible_resources(self, access_token: str) -> list:
        """Get list of Jira sites accessible with the access token.
        
        Args:
            access_token: OAuth access token
            
        Returns:
            List of accessible resources
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.atlassian.com/oauth/token/accessible-resources",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            response.raise_for_status()
            return response.json()
    
    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get authenticated user information.
        
        Args:
            access_token: OAuth access token
            
        Returns:
            User information
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.atlassian.com/me",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            response.raise_for_status()
            return response.json()
