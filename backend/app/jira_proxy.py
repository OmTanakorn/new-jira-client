"""Jira API proxy logic for handling complex operations."""
from typing import Dict, Any, List
from app.utils.jira_client import JiraClient
from app.utils.transformers import transform_issues, transform_projects
from app.models import JiraSearchRequest, IssueTransitionRequest, IssueUpdateRequest


async def search_issues_proxy(
    search_request: JiraSearchRequest,
    jira_client: JiraClient
) -> Dict[str, Any]:
    """Proxy for searching Jira issues with transformation.
    
    Args:
        search_request: Search request parameters
        jira_client: Authenticated Jira client
        
    Returns:
        Transformed search results
    """
    result = await jira_client.search_issues(
        jql=search_request.jql,
        fields=search_request.fields,
        max_results=search_request.max_results,
        start_at=search_request.start_at
    )
    
    # Transform issues to simplified format
    issues = result.get("issues", [])
    transformed_issues = transform_issues(issues)
    
    return {
        "issues": transformed_issues,
        "total": result.get("total", 0),
        "start_at": result.get("startAt", 0),
        "max_results": result.get("maxResults", 0),
    }


async def get_projects_proxy(jira_client: JiraClient) -> List[Dict[str, Any]]:
    """Proxy for getting Jira projects with transformation.
    
    Args:
        jira_client: Authenticated Jira client
        
    Returns:
        Transformed list of projects
    """
    projects = await jira_client.get_projects()
    return transform_projects(projects)


async def transition_issue_proxy(
    issue_key: str,
    transition_request: IssueTransitionRequest,
    jira_client: JiraClient
) -> Dict[str, Any]:
    """Proxy for transitioning an issue.
    
    Args:
        issue_key: Issue key (e.g., 'PROJ-123')
        transition_request: Transition request parameters
        jira_client: Authenticated Jira client
        
    Returns:
        Result of the transition operation
    """
    result = await jira_client.transition_issue(
        issue_key=issue_key,
        transition_id=transition_request.transition_id
    )
    
    return {
        "success": True,
        "issue_key": issue_key,
        "transition_id": transition_request.transition_id,
    }


async def update_issue_proxy(
    issue_key: str,
    update_request: IssueUpdateRequest,
    jira_client: JiraClient
) -> Dict[str, Any]:
    """Proxy for updating issue fields.
    
    Args:
        issue_key: Issue key (e.g., 'PROJ-123')
        update_request: Update request parameters
        jira_client: Authenticated Jira client
        
    Returns:
        Result of the update operation
    """
    result = await jira_client.update_issue(
        issue_key=issue_key,
        fields=update_request.fields
    )
    
    return {
        "success": True,
        "issue_key": issue_key,
        "fields": update_request.fields,
    }


async def get_issue_proxy(
    issue_key: str,
    jira_client: JiraClient
) -> Dict[str, Any]:
    """Proxy for getting issue details.
    
    Args:
        issue_key: Issue key (e.g., 'PROJ-123')
        jira_client: Authenticated Jira client
        
    Returns:
        Issue details
    """
    issue = await jira_client.get_issue(issue_key)
    
    # Return full issue data for detail view
    return issue
