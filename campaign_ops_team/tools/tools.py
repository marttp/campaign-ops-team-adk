from google.adk.tools.function_tool import FunctionTool


def _internal_data_agent_tool(query: str) -> dict:
    """
    Provides company-wide FinTech KPIs and daily-used product features for use by agents.
    This tool acts as the unified internal data source for Intake, Planner, and Critic agents.

    It returns:
    - The full list of company-wide KPIs (DAU, GMV, success rate, monetization metrics, etc.)
    - The full list of commonly-used FinTech features (P2P transfer, QR payments, bill payment, etc.)

    Query Behavior:
        The `query` parameter is included for future semantic lookup or filtering,
        but in this current version it returns the full dataset regardless of the query.
        Agents typically pass values like "metrics", "features", "payments", or
        "company health" when requesting internal references.

    Intended Use:
        • The Intake Agent uses this tool to understand platform context, goals, and constraints.
        • The Planner/Marketing group uses it to estimate feasibility, segment behavior, and strategic planning.
        • Critic Agents use it to validate assumptions, detect contradictions, and score plan quality.
        • The Reporter Agent may compact or summarize this data before passing to Delivery.

    Args:
        query (str): A keyword or phrase used to request relevant internal data.
                     Currently not used for filtering, but included for forward compatibility.

    Returns:
        dict: A dictionary containing:
            - all_kpis: List of company-wide KPIs relevant to FinTech business performance.
            - all_features: List of top daily-used FinTech features with metadata
                            (category, goal, monetization logic, user journey).
    """

    # -------------------------
    # Company-wide KPIs (5)
    # -------------------------
    company_wide_kpis = [
        {
            "id": "active_users_dau",
            "name": "Daily Active Users",
            "description": "Unique users who performed at least one meaningful action today.",
            "reason": "Reflects overall platform health, engagement, and retention.",
        },
        {
            "id": "transaction_volume_gmv",
            "name": "Total Payment Volume (GMV)",
            "description": "Sum of all financial transactions processed on the platform.",
            "reason": "Primary revenue driver via fees and commissions.",
        },
        {
            "id": "txn_success_rate",
            "name": "Transaction Success Rate",
            "description": "Percentage of successful transactions out of attempted ones.",
            "reason": "Impacts trust, support load, and regulatory audits.",
        },
        {
            "id": "revenue_per_user_arpau",
            "name": "Average Revenue Per Active User (ARPAU)",
            "description": "Revenue divided by active user count.",
            "reason": "Represents monetization efficiency.",
        },
        {
            "id": "activation_conversion_rate",
            "name": "Activation Conversion Rate",
            "description": "Percentage of new users who complete onboarding or first transaction.",
            "reason": "Critical indicator for funnel efficiency and quarterly growth.",
        },
    ]

    # -------------------------
    # Daily-used FinTech features (7)
    # -------------------------
    fintech_features = [
        {
            "id": "send_money_p2p",
            "name": "P2P Money Transfer",
            "category": "payments",
            "goal": "Allow users to instantly send money to friends or family.",
            "why_it_profit": "Drives engagement and increases wallet balance retention.",
            "brief_user_journey": "User selects contact → enters amount → confirms transfer.",
        },
        {
            "id": "qr_payment_offline",
            "name": "QR Code Payment (Offline Merchants)",
            "category": "merchant_payment",
            "goal": "Enable quick and frictionless in-store payments.",
            "why_it_profit": "High-frequency use generates transaction fees and repeat DAU.",
            "brief_user_journey": "User scans QR → enters amount → pays.",
        },
        {
            "id": "bill_payments",
            "name": "Utility & Bill Payments",
            "category": "services",
            "goal": "Provide a hub for paying recurring bills.",
            "why_it_profit": "Earns commission from billers and improves monthly retention.",
            "brief_user_journey": "User selects provider → enters account → pays.",
        },
        {
            "id": "topup_mobile",
            "name": "Mobile Top-Up",
            "category": "services",
            "goal": "Let users top-up phone credit or data.",
            "why_it_profit": "Brings commission revenue and encourages wallet loading.",
            "brief_user_journey": "User picks telco → enters number → selects amount → pays.",
        },
        {
            "id": "cashback_rewards",
            "name": "Cashback Rewards & Vouchers",
            "category": "growth",
            "goal": "Boost repeated spending and merchant engagement.",
            "why_it_profit": "Increases GMV and merchant campaign revenues.",
            "brief_user_journey": "User activates voucher → makes purchase → gets cashback.",
        },
        {
            "id": "transaction_history",
            "name": "Transaction History & Insights",
            "category": "core_app",
            "goal": "Provide transparent logs of user spending.",
            "why_it_profit": "Reduces customer support load and increases trust.",
            "brief_user_journey": "User opens history → filters → views details.",
        },
        {
            "id": "linked_bank_transfer",
            "name": "Bank Transfer / Withdrawal",
            "category": "banking",
            "goal": "Allow money transfer between wallet and bank accounts.",
            "why_it_profit": "Encourages wallet loading and increases stored balance.",
            "brief_user_journey": "User selects bank → enters amount → confirms.",
        },
    ]

    return {
        "all_kpis": company_wide_kpis,
        "all_features": fintech_features,
    }


internal_data_agent_tool = FunctionTool(func=_internal_data_agent_tool)


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
