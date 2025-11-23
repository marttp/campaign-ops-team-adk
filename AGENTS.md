# Campaign Ops Agent - ADK Python Version

## Overview
The Campaign Ops Agent is a multi-agent system built in Python using Google's Agent Development Kit (ADK). Its purpose is to automate the end-to-end planning and orchestration of marketing campaigns for businesses. Marketing teams often struggle to coordinate segmentation, channel planning, scheduling, and delivery while tracking historical performance. This agent orchestrates those tasks, freeing marketing ops teams from manual coordination and reducing campaign errors.

## Business Use Case
Marketing teams repeatedly create campaigns to promote products or services. Each campaign starts with a brief that contains objectives, key performance indicators (KPIs), audience definitions, and constraints. Teams must translate that brief into a structured campaign plan: who to target, which channels to use (email, push, SMS), when to send, and how to avoid overlapping campaigns. They also need to generate the data payload for the delivery system. Historically this work is done manually across multiple tools and often leads to errors, wasted spend, and inconsistent targeting. The Campaign Ops Agent solves this by automating segmentation, planning, risk checks, and specification generation.

## Multi-Agent Architecture
The system consists of an orchestrator and a set of specialized agents grouped by function. Grouping agents allows the design to scale while meeting ADK requirements for multi-agent systems. Each agent group can contain one or more underlying agents depending on complexity.

### Group 1: Segment Group
Responsible for parsing the campaign brief, extracting objectives, identifying target segments, and enriching them with additional filters.

- **Intake & Segmentation Agent**: Powered by an LLM to interpret unstructured briefs, extract KPIs and constraints, and build audience segments via queries to customer data stores using the Agent Tool interface.

### Group 2: Planner & Scheduling Group
Plans channels, cadence, and delivery schedules while checking for conflicts with existing campaigns.

- **Planning Agent**: Chooses channels and schedules send times based on rules, channel capacity, and user preferences.
- **Risk Agent**: Runs in parallel to the planner agent to detect audience collisions, regulatory constraints, and schedule conflicts, then recommends adjustments. These agents demonstrate parallel, sequential, and loop patterns: the planner and risk agents operate concurrently, and the orchestrator may loop back to recalculate if the risk agent flags a conflict.

### Group 3: Delivery Group
Generates the final artifacts needed by backend services.

- **Export Agent**: Composes a structured campaign specification, including target user IDs or attributes, channel payloads, and schedules, and writes it to the required backend (e.g., a CRM or message delivery API).

## Orchestrator Responsibilities
Manages the overall workflow. It holds a session object for each campaign, passes intermediate results between groups, and persists long-term learnings (via a memory service) about successful segments, channel rules, and collision patterns. It also logs and traces every agent call for observability.

## Key ADK Concepts Demonstrated
- **Multi-agent design**: Separate agents manage segmentation, planning, risk checking, and export. They can run sequentially and in parallel, with loopback if risk detection triggers a re-plan.
- **LLM-powered agents**: The Intake & Segmentation Agent uses an LLM to summarize the brief and define segments.
- **Tool integration**: Agents call external tools via ADK's Model Context Protocol (MCP), including customer database APIs for segmentation, calendar APIs for scheduling, and CRM APIs for exporting the campaign spec.
- **Sessions & memory**: The orchestrator uses an in-memory session service to keep per-campaign context. A Memory Bank stores long-term knowledge (e.g., past segments, channel rules) for context engineering.
- **Observability**: Every agent call logs its inputs, outputs, and tool results. Traces show the chain of decisions, and metrics expose success/error rates to support agent evaluation and debugging.
- **Agent-to-Agent Protocol (A2A)**: Agents communicate via orchestrator-passed messages. The risk agent can send a message back to the planner agent to trigger a re-planning loop.
- **Deployment**: The architecture can be deployed to Vertex AI Agent Engine or another runtime. Each group can scale independently, and the orchestrator centralizes state and error handling.

## Using This Agent with ADK (Python)
1. **Define agent classes**: Create Python classes for `CampaignOrchestrator`, `IntakeSegmentationAgent`, `PlanningAgent`, `RiskAgent`, and `ExportAgent` using the ADK base classes. Implement `run()` to handle input messages and call tools via MCP.
2. **Implement tools**: Define OpenAPI or custom tool functions for database queries, channel scheduling, risk checking, and export. Register them with the ADK environment.
3. **Configure session and memory services**: Use `InMemorySessionService` for per-campaign state and `MemoryBank` for long-term storage. Provide keys to identify each campaign session.
4. **Add observability**: Initialize logging, tracing, and metrics in your agent classes. Use ADK's evaluation hooks or integrate an LLM-as-judge to score segment quality.
5. **Deploy**: Package the agent system as a service and deploy to Vertex AI Agent Engine or a comparable environment. The orchestrator listens for new campaign briefs and coordinates the agents.

## Conclusion
The Campaign Ops Agent demonstrates a practical multi-agent architecture for automating marketing campaign orchestration. It implements multi-agent sequencing, tool integration, session and memory management, observability and evaluation, agent-to-agent communication, and a clear deployment path. The outcome is a strong business case: reducing manual overhead, minimizing campaign collisions, and improving targeting accuracy, which translates into a better return on marketing spend.

