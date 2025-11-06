"""Data transformation utilities for converting Jira data to frontend-friendly format."""
from typing import Dict, Any, List, Optional


def transform_issue(issue: Dict[str, Any]) -> Dict[str, Any]:
    """Transform Jira issue to simplified format.
    
    Args:
        issue: Raw issue data from Jira API
        
    Returns:
        Simplified issue data for frontend
    """
    fields = issue.get("fields", {})
    
    return {
        "key": issue.get("key", ""),
        "summary": fields.get("summary", ""),
        "status": fields.get("status", {}).get("name", ""),
        "assignee": fields.get("assignee", {}).get("displayName") if fields.get("assignee") else None,
        "priority": fields.get("priority", {}).get("name") if fields.get("priority") else None,
        "issue_type": fields.get("issuetype", {}).get("name", ""),
        "description": fields.get("description"),
    }


def transform_issues(issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Transform list of Jira issues.
    
    Args:
        issues: List of raw issue data from Jira API
        
    Returns:
        List of simplified issue data
    """
    return [transform_issue(issue) for issue in issues]


def transform_project(project: Dict[str, Any]) -> Dict[str, Any]:
    """Transform Jira project to simplified format.
    
    Args:
        project: Raw project data from Jira API
        
    Returns:
        Simplified project data
    """
    return {
        "id": project.get("id", ""),
        "key": project.get("key", ""),
        "name": project.get("name", ""),
    }


def transform_projects(projects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Transform list of Jira projects.
    
    Args:
        projects: List of raw project data from Jira API
        
    Returns:
        List of simplified project data
    """
    return [transform_project(project) for project in projects]
