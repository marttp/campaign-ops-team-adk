# Campaign Ops Agent

## Description

The Campaign Ops Agent is a production-style, multi-agent orchestration pipeline built with Google's Agent Development Kit (ADK). It mirrors how real marketing teams operate (Frontline intake -> Planner/Marketing strategy -> Delivery execution) but runs each step with specialized AI agents. The Campaign Ops Orchestrator governs flow control, announces each stage to the user, ensures agents recommend missing metrics without halting for input, and escalates results downstream.

- **Frontline Group**: Looping Intake and Critic agents interpret the user goal, call the internal data tool (now packed with mock KPIs for a 1,000-user scale), and output an approved frontline brief that includes goal hypotheses plus best/average/worst scenarios. A Frontline Evidence agent compacts this into a structured JSON contract.
- **Planner Group**: Goal Planning, Segmentation Discovery, and Planner Critic agents iterate (bounded loop) until the campaign charter is ready. Instructions demand persuasive consumer content (campaign name/theme/hero promise, offers like "Spend 10K THB this month, unlock 5% cashback on 10 rides next month"), quantified KPI targets, segment definitions with eligibility + offer copy, and a delivery-ready JSON contract assembled by the Reporter.
- **Delivery Group**: A ParallelAgent runs Eligibility, Email, and Push specialists simultaneously. Each agent calls locally defined tools to configure audiences or craft content, infers missing creative from planner outputs, and registers its work via a mock `campaign_creation_tool`. A Delivery Aggregator then merges `planner_result` with channel outputs, surfacing KPIs, schedule, and creation events for final reporting.

This architecture demonstrates how ADK can power a modular marketing ops stack with deterministic handoffs, structured tool usage, and production-friendly prompts. The repo includes local mock tools so the system is self-contained for demos, plus deployment scripts for ADK agent engines.

## Command

### ADK Web

```bash
uv run adk web
```

### Deploy Agent Engine

```bash
uv run adk deploy agent_engine campaign_ops_team --agent_engine_config_file=campaign_ops_team/.agent_engine_config.json --trace_to_cloud
```

### Deploy Agent Engine - Express Mode

```bash
uv run adk deploy agent_engine campaign_ops_team --api_key=[api_key] --agent_engine_config_file=campaign_ops_team/.agent_engine_config.json --trace_to_cloud
```

### Test connection - Agent Engine

```bash
uv run manual_operations/test.py
```

### Clean up - Agent Engine

```bash
uv run manual_operations/clean_up.py
```
