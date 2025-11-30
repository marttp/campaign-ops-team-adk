from google.adk.tools.function_tool import FunctionTool


def _segment_group_preparing_tool(segment_criteria: str) -> str:
    """Creates segment definitions for the audience system."""
    return f"Segment Prepared: [Mock] Segment defined by {segment_criteria}."


segment_group_preparing_tool = FunctionTool(func=_segment_group_preparing_tool)


def _find_audience_tool(criteria: str) -> str:
    """Queries or simulates audience retrieval."""
    return f"Audience Found: [Mock] 50,000 users match {criteria}."


find_audience_tool = FunctionTool(func=_find_audience_tool)


def _create_audience_tool(audience_name: str, criteria: str) -> str:
    """Registers final audience."""
    return f"Audience Created: [Mock] ID: 12345, Name: {audience_name}."


create_audience_tool = FunctionTool(func=_create_audience_tool)


def _eligibility_tool(rules: str) -> str:
    """Prepares user attribute rules."""
    return f"Eligibility Rules Set: [Mock] {rules}."


eligibility_tool = FunctionTool(func=_eligibility_tool)


def _email_tool(template_id: str, content: str) -> str:
    """Formats email message payloads."""
    return f"Email Payload: [Mock] Template {template_id} with content '{content}'."


email_tool = FunctionTool(func=_email_tool)


def _push_notification_tool(title: str, body: str) -> str:
    """Formats push notification payloads."""
    return f"Push Payload: [Mock] Title: {title}, Body: {body}."


push_notification_tool = FunctionTool(func=_push_notification_tool)


def _campaign_creation_tool(campaign_name: str, details: str) -> str:
    """Final deterministic wrapper that creates a unified campaign JSON."""
    return f"Campaign Created: [Mock] Name: {campaign_name}, Status: Scheduled."


campaign_creation_tool = FunctionTool(func=_campaign_creation_tool)


def exit_loop():
    """Call this function ONLY when the critique is 'APPROVED', indicating the story is finished and no more changes are needed."""
    return {"status": "approved"}


exit_loop_tool = FunctionTool(func=exit_loop)
