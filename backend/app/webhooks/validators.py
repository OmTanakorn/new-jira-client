"""Webhook payload validators."""
from typing import Dict, Any


def validate_webhook_payload(payload: Dict[str, Any]) -> bool:
    """Validate Jira webhook payload structure.
    
    Args:
        payload: Webhook payload from Jira
        
    Returns:
        True if payload is valid
    """
    # Basic validation - check for required fields
    if "webhookEvent" not in payload:
        return False
    
    # Validate event type
    valid_events = [
        "jira:issue_created",
        "jira:issue_updated",
        "jira:issue_deleted",
    ]
    
    webhook_event = payload.get("webhookEvent")
    if webhook_event not in valid_events:
        return False
    
    # Issue events should have issue data
    if webhook_event.startswith("jira:issue"):
        if "issue" not in payload:
            return False
    
    return True
