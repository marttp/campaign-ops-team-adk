from google.adk.agents import LlmAgent, LoopAgent, SequentialAgent
from google.adk.models import Gemini
from google.adk.tools.function_tool import FunctionTool

MODEL = "gemini-2.5-flash-lite"


def internal_data_agent_tool(query: str) -> dict:
    """
    Provides company-wide FinTech KPIs and daily-used product features for use by agents.
    This tool acts as the unified internal data source for Intake, Planner, and Critic agents.

    It returns:
    - The full list of company-wide KPIs (DAU, GMV, success rate, monetization metrics, etc.)
    - The full list of commonly-used FinTech features (P2P transfer, QR payments, bill payment, etc.)
    - A `mock_current_kpis` section that surfaces current baselines for a 1,000-user scale app so
      Planner agents can set concrete KPI deltas and thresholds.

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

    # -------------------------
    # Mock KPI baselines for a 1,000-user scale
    # -------------------------
    mock_current_kpis = [
        {
            "metric": "monthly_active_users",
            "value": 1000,
            "unit": "users",
            "comment": "Reference cohort size for campaign modeling.",
        },
        {
            "metric": "avg_txn_per_user_month",
            "value": 8.2,
            "unit": "transactions/user/month",
            "comment": "All channels blended frequency.",
        },
        {
            "metric": "qr_txn_share",
            "value": 0.35,
            "unit": "share",
            "comment": "35% of transactions are QR merchant payments.",
        },
        {
            "metric": "avg_monthly_spend",
            "value": 4200,
            "unit": "THB/user/month",
            "comment": "Wallet plus linked bank spend on-platform.",
        },
        {
            "metric": "high_value_segment_size",
            "value": 180,
            "unit": "users",
            "comment": ">=10,000 THB monthly spend in last 90 days.",
        },
        {
            "metric": "cashback_redemption_rate",
            "value": 0.22,
            "unit": "rate",
            "comment": "Share of users who redeem at least one voucher per month.",
        },
    ]

    return {
        "all_kpis": company_wide_kpis,
        "all_features": fintech_features,
        "mock_current_kpis": mock_current_kpis,
    }


def exit_loop():
    """Call this function ONLY when the critique is 'APPROVED', indicating the analysis is finished and no more changes are needed."""
    return {"status": "approved"}


# Intake Agent
intake_agent = LlmAgent(
    name="intake_agent",
    model=Gemini(model=MODEL),
    description="Discover possible features that fit the goal of the user request by taking a look in internal metrics and product features.",
    instruction="""
    You are the Intake Agent. Your goal is to discover possible features that fit the goal of the user request.
    User will provide a short metric goal or complex goal. Your work will be to find the best possible features that fit the goal.
    Use the `internal_data_agent_tool` to get context about product features and company metrics.

    If you receive a critique, refine your previous proposal based on it.

    Response MUST follow and response all below concerns
    - goal (short metric goal or complex goal)
    - possible_features (list of product features that could be involved in this campaign)
    - best_case (optimistic outcome scenario if the campaign performs exceptionally well)
    - worst_case (negative outcome scenario if the campaign fails or underperforms)
    - average_case (expected or most likely outcome scenario under typical conditions)
    """,
    tools=[FunctionTool(func=internal_data_agent_tool)],
    output_key="intake_result",
)

# Frontline Critic Agent
frontline_critic_agent = LlmAgent(
    name="frontline_critic_agent",
    model=Gemini(model=MODEL),
    description="Evaluates the Intake Agent's output.",
    instruction="""
    You are the Frontline Critic Agent. Your goal is to evaluate the Intake Agent's output for realism, missing elements, and conflicts.
    Evaluate the latest proposal.
    If the intake is good, output "APPROVED" and call the `exit_loop` tool.
    If there are issues, explain them clearly so the intake agent can fix them.
    """,
    tools=[FunctionTool(func=exit_loop)],
    output_key="critique",
)


product_market_estimation_loop = LoopAgent(
    name="ProductMarketEstimationLoop",
    sub_agents=[intake_agent, frontline_critic_agent],
    max_iterations=2,  # Prevents infinite loops
)

frontline_evidence_agent = LlmAgent(
    name="frontline_evidence_agent",
    model=Gemini(model=MODEL),
    description="Gathers evidence to support final feature selection.",
    instruction="""
    You are the final Frontline agent before the Planner group receives context. Take the latest
    approved intake package and produce a structured summary.

    Response MUST follow and response all below concerns
    - goal (short metric goal or complex goal)
    - possible_features (list of product features that could be involved in this campaign)
    - best_case (optimistic outcome scenario if the campaign performs exceptionally well)
    - worst_case (negative outcome scenario if the campaign fails or underperforms)
    - average_case (expected or most likely outcome scenario under typical conditions)
    """,
    output_key="frontline_result",
)

# Frontline Manager Agent
frontline_manager_agent = SequentialAgent(
    name="frontline_manager_agent",
    sub_agents=[product_market_estimation_loop, frontline_evidence_agent],
)
