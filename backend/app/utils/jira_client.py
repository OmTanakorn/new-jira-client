"""Jira API client wrapper."""
import httpx
from typing import Optional, Dict, Any, List
import os


class JiraClient:
    """HTTP client for Jira API interactions."""
    
    def __init__(self, base_url: Optional[str] = None, access_token: Optional[str] = None):
        """Initialize Jira client.
        
        Args:
            base_url: Jira instance base URL
            access_token: OAuth access token for authenticated requests
        """
        self.base_url = base_url or os.getenv("JIRA_BASE_URL", "")
        self.access_token = access_token
        self.client = httpx.AsyncClient(timeout=30.0)
        
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authorization."""
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        return headers
    
    async def search_issues(
        self,
        jql: str,
        fields: Optional[List[str]] = None,
        max_results: int = 50,
        start_at: int = 0
    ) -> Dict[str, Any]:
        """Search for issues using JQL.
        
        Args:
            jql: JQL query string
            fields: List of fields to return
            max_results: Maximum number of results
            start_at: Starting index for pagination
            
        Returns:
            Search results from Jira API
        """
        url = f"{self.base_url}/rest/api/3/search"
        payload = {
            "jql": jql,
            "maxResults": max_results,
            "startAt": start_at,
        }
        if fields:
            payload["fields"] = fields
            
        response = await self.client.post(
            url,
            json=payload,
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    async def get_issue(self, issue_key: str) -> Dict[str, Any]:
        """Get details for a specific issue.
        
        Args:
            issue_key: Issue key (e.g., 'PROJ-123')
            
        Returns:
            Issue details from Jira API
        """
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}"
        response = await self.client.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    async def transition_issue(
        self,
        issue_key: str,
        transition_id: str
    ) -> Dict[str, Any]:
        """Transition an issue to a new status.
        
        Args:
            issue_key: Issue key (e.g., 'PROJ-123')
            transition_id: ID of the transition to execute
            
        Returns:
            Response from Jira API
        """
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}/transitions"
        payload = {"transition": {"id": transition_id}}
        response = await self.client.post(
            url,
            json=payload,
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json() if response.content else {}
    
    async def update_issue(
        self,
        issue_key: str,
        fields: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update issue fields.
        
        Args:
            issue_key: Issue key (e.g., 'PROJ-123')
            fields: Dictionary of fields to update
            
        Returns:
            Response from Jira API
        """
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}"
        payload = {"fields": fields}
        response = await self.client.put(
            url,
            json=payload,
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json() if response.content else {}
    
    async def get_projects(self) -> List[Dict[str, Any]]:
        """Get list of accessible projects.
        
        Returns:
            List of projects from Jira API
        """
        url = f"{self.base_url}/rest/api/3/project"
        response = await self.client.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    async def get_transitions(self, issue_key: str) -> List[Dict[str, Any]]:
        """Get available transitions for an issue.
        
        Args:
            issue_key: Issue key (e.g., 'PROJ-123')
            
        Returns:
            List of available transitions
        """
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}/transitions"
        response = await self.client.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json().get("transitions", [])
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
