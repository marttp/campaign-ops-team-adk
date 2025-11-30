# Campaign Ops Agent

## Problem

Marketing teams routinely juggle fragmented spreadsheets, creative briefs, and execution tickets when planning campaigns. Objectives, segmentation logic, and channel payloads are often disconnected, leading to slow iterations, unclear KPIs, and error-prone handoffs to channel teams. The process breaks down further when teams lack easy access to baseline metrics or must coordinate across multiple tool stacks.

## Solution

The Campaign Ops Agent is a production-style, multi-agent orchestration pipeline built with Google's Agent Development Kit (ADK). It mirrors real marketing organizations (Frontline intake → Planner/Marketing strategy → Delivery execution) and assigns each stage to specialized AI agents. The Campaign Ops Orchestrator:

- Announces each stage to the user and shares status updates
- Instructs agents to recommend missing metrics using mock KPI baselines for a 1,000-user app
- Enforces bounded loops (intake/critic, goal/segment/critic) to refine outputs without delaying the user
- Passes structured JSON contracts between groups so downstream agents never guess

## Architecture Overview

![Architecture](AI%20Architecture.jpg)

1. **Frontline Group** – Looping Intake and Critic agents interpret goals, call the internal data tool, and output best/average/worst-case hypotheses. A Frontline Evidence agent compacts the approved package into `frontline_result`.
2. **Planner Group** – Goal Planning, Segmentation Discovery, and Planner Critic agents iterate until a charter is feasible. The Reporter emits the `planner_result` JSON containing campaign name/theme/hero promise, segments, KPI targets, schedule, delivery briefs, and risks.
3. **Delivery Group** – A ParallelAgent runs Eligibility, Email, and Push specialists concurrently. Each agent uses local mock tools to configure audiences or craft content, registers a creation event, and sends outputs to a Delivery Aggregator that returns the final execution packet.

This design keeps the repo self-contained (all mock tools live in-code) while showcasing ADK primitives such as `SequentialAgent`, `LoopAgent`, `ParallelAgent`, and agent-to-agent tool calls.

## Setup Instructions

1. **Install dependencies**
   ```bash
   uv sync
   ```
2. **Configure environment** – Set `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`, and any ADK credentials required by your deployment target.
3. **Run locally (ADK web sandbox)**
   ```bash
   uv run adk web
   ```
4. **Deploy to Vertex AI Agent Engine**
   ```bash
   uv run adk deploy agent_engine campaign_ops_team \
     --agent_engine_config_file=campaign_ops_team/.agent_engine_config.json \
     --trace_to_cloud
   ```
5. **Express deploy (API key)**
   ```bash
   uv run adk deploy agent_engine campaign_ops_team \
     --api_key=[api_key] \
     --agent_engine_config_file=campaign_ops_team/.agent_engine_config.json \
     --trace_to_cloud
   ```
6. **Manual test** – Streams responses until Ctrl+C to mimic ADK web behavior.
   ```bash
   uv run manual_operations/test.py
   ```
7. **Clean up**
   ```bash
   uv run manual_operations/clean_up.py
   ```

## Additional Notes

- `PROJECT_DESCRIPTION.md` contains a concise writeup of the system for submissions.
- `AI Architecture.jpg` illustrates the Frontline → Planner → Delivery pipeline.
- All Planner and Delivery tools are mocked locally so demos run without external dependencies.

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
