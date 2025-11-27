# Campaign Ops Agent

## Description

The Campaign Ops Agent is a Python system built with Google's Agent Development Kit that automates how marketing teams turn campaign briefs into executable plans. An orchestrator coordinates segmentation, planning, risk analysis, and export groups while sharing per-campaign sessions and drawing on a memory bank of past insights. The Intake & Segmentation Agent interprets objectives, KPIs, and constraints, then enriches audiences through MCP-connected data stores. Planning and Risk agents run concurrently to select channels, schedule sends, and loop when conflicts appear. Finally, the Export Agent assembles delivery-ready specifications, logging every step for observability, evaluation, and scalable deployment for marketing stakeholders.


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

