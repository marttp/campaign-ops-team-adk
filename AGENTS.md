# Campaign Ops Agent – ADK Python Version

## Overview

The Campaign Ops Agent is a multi-agent system built in Python using Google's Agent Development Kit (ADK). Its purpose is to automate the end-to-end planning and orchestration of marketing campaigns for businesses. Marketing teams often struggle to coordinate segmentation, channel planning, scheduling, and content delivery while tracking historical performance. This agent orchestrates those tasks across multiple sub-agents.

This system follows a strict sequential pipeline:

Frontline Group → Planner/Marketing Group → Delivery Group

Each group contains specialized agents, and the Campaign Ops Orchestrator coordinates the whole workflow. The Reporter Agent in the Planner group is the final step before passing outputs downstream.

This document outlines the multi-agent architecture, agent behaviors, memory, tools, and coordination logic.

## Agent Groups

### 1. Frontline Group (3 agents)
These agents interpret raw campaign requests, contextual data, and usage metrics.

**Agents:**
- **Intake Agent**  
  Extracts campaign type, objectives, rough segmentation hypotheses, and constraints.

- **Frontline Critic Agent**  
  Domain-specific evaluation for frontline context.  
  Ensures the Intake Agent’s output is meaningful and consistent with product metrics.

**Tools used:**
- Internal Data Agent tool (product features, company metrics)

**Looping behavior:**
- Intake Agent → Critic → (optional loop for refinement) → finalize intake package

---

### 2. Planner/Marketing Group
Transforms abstract goals into actionable segmentation, scheduling, and delivery plans.

**Agents:**
- **Goal Planning Agent**  
  Converts frontline output into structured goals, KPIs, and scheduling intent.

- **Segmentation Discovery Agent**  
  Generates segments, rules, estimate sizes, explores customer behavior.

- **Planner Critic Agent**  
  A specialist critic validating strategy feasibility, conflicts, and quality.

- **Google Search Agent**  
  Supports competitive research, seasonal patterns, industry insights.

- **Reporter Agent (final agent of the group)**  
  The last step of Planner group.  
  Validates downstream requirements, compacts context, and produces a structured, orchestrator-ready JSON summary.

**Loop behavior:**
Goal Planning Agent → Segmentation Discovery → Planner Critic → Loop if needed → Reporter (final)

**Reporter Output Contract:**
The Reporter produces a clean JSON object including:
- campaign_type  
- primary and secondary goals  
- discovered segments  
- audience size  
- constraints  
- schedule plan  
- risks & confidence estimates  
- references to audience tools  
- normalized plan for the Delivery group

This output is guaranteed to be the Planner group’s final deliverable.

---

### 3. Delivery Group
Transforms the Planner group’s final plan into execution-ready artifacts.

**Agent:**
- **Delivery Agent**  
  Coordinates tools to prepare user attributes, email/push payloads, and final campaign components.

**Tools:**
- **Eligibility Tool**  
  Produces user attributes or eligibility filters.

- **Email Tool**  
  Builds email payload templates.

- **Push Notification Tool**  
  Builds push payload templates.

- **Segment Group Preparing Tool**  
  Structures segments for audience creation.

- **Find Audience Tool**  
  Determines eligible users.

- **Create Audience Tool**  
  Generates final campaign audience.

- **Campaign Creation Tool**  
  Final orchestrated output: produces the final campaign object ready for execution in downstream systems.

Delivery Agent → tools → final campaign payload

---

## Orchestrator: Campaign Ops Orchestrator

The orchestrator governs:

1. Flow control  
2. Group-to-group sequencing  
3. Context propagation  
4. Loop bounding (max iterations per group)  
5. Logging, metrics, and memory  

Flow diagram:

Frontline Group → Planner Reporter Agent → Delivery Group → Final Output

Each group passes a structured JSON to the next group.

---

## Memory & Sessions

### Session Service
Maintains the conversation state per campaign creation process.

Includes:
- campaign_type  
- constraints  
- segment hypotheses  
- planner outputs  
- delivery outputs

### Memory Bank
Stores long-term reusable knowledge:
- past campaign configurations  
- best/worst/average performance references  
- naming conventions  
- historical risk patterns  
- audiences previously used  
- content schemas

Reporter Agent performs **context compaction** before passing to the next group, ensuring memory and session stay lightweight.

---

## Tools Summary

**Product Features Tool**  
Returns up-to-date product metadata.

**Company-wide Metric Tool**  
Returns KPIs, performance metrics, MAU/DAU, etc.

**Internal Data Agent Tool**  
Merges product & metric tools into a frontend-ready info set.

**Google Search Tool**  
Queries external data for campaign ideation.

**Segment Group Preparing Tool**  
Creates segment definitions for the audience system.

**Find Audience Tool**  
Queries or simulates audience retrieval.

**Create Audience Tool**  
Registers final audience.

**Eligibility Tool**  
Prepares user attribute rules.

**Email Tool**  
Formats email message payloads.

**Push Tool**  
Formats push notification payloads.

**Campaign Creation Tool**  
Final deterministic wrapper that creates a unified campaign JSON.

---

## Agent Prompts (High-Level)

### Intake Agent
“Extract goals, constraints, segments hypotheses. Use company metrics provided by tools.”

### Frontline Critic Agent
“Evaluate intake output: realism, missing elements, conflicts.”

### Goal Planning Agent
“Convert intake package into structured goals, scheduling intent, KPI expectations.”

### Segmentation Discovery Agent
“Generate actionable segments, eligibility rules, size estimation.”

### Planner Critic Agent
“Evaluate strategic and scheduling feasibility, performance estimates.”

### Google Search Agent
“Gather competitive and industry insights for Planner group.”

### Reporter Agent
“You are the final agent of the Planner group. Produce a clean, validated, normalized JSON for delivery. Compact context. Ensure no missing fields.”

### Delivery Agent
“Use tools to build eligibility, email, push, and final campaign payload. Produce final campaign object.”

---

## Execution Flow Summary

1. Orchestrator calls Frontline Group.  
2. Frontline Group loops until Critic is satisfied.  
3. Orchestrator passes result into Planner Group.  
4. Planner Group loops until Critic is satisfied.  
5. Reporter Agent generates final summary.  
6. Orchestrator passes Reporter output to Delivery Group.  
7. Delivery Agent calls all required tools.  
8. Campaign Creation Tool produces final execution payload.  
9. Orchestrator stores summary to Memory Bank.  
10. Final output returned to user/system.

---

## Implementation Notes (ADK Python)

- Each agent is implemented as an `Agent` object.  
- Tools are Python functions exposed through ADK.  
- Groups are orchestrated in Python via sequential workflows.  
- Critic loops must be bounded (max 2–3 iterations).  
- Reporter Agent is the *official exit* of the Planner group.  
- Delivery sub-agents are tools, not agents.  
- Memory Bank and Session Service maintain state.  
- The Orchestrator is a Python class coordinating all steps.

---

## Conclusion

This multi-agent design provides a clean, production-ready orchestration model aligned with modern agent engineering principles. The Frontline, Planner, and Delivery groups each encapsulate specialized responsibility, with Reporter Agent acting as the final structured output provider for planning. The architecture is modular, scalable, and well-structured for both capstone demonstration and real-world enterprise use.
