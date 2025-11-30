# Campaign Ops Agent

## Overview
The **Campaign Ops Agent** is a production-grade, multi-agent orchestration system built with Google's Agent Development Kit (ADK). It turns campaign planning into a disciplined pipeline—**Frontline intake**, **Planner strategy**, **Delivery execution**—so marketers get a complete plan without juggling spreadsheets or copy decks.

The Campaign Ops Orchestrator sequences every stage, announces each transition to the user, and instructs agents to fill in missing metrics using mock KPI baselines for a 1,000-user app. The flow never stalls midstream; only the final output may ask for confirmation.

## Frontline Group
Frontline Group runs Intake and Critic agents in a loop, then a Frontline Evidence agent.
*   **Intake Agent**: Interprets the goal, calls the internal data tool for KPIs + feature inventory, and outputs goal hypotheses plus best/worst/average scenarios.
*   **Critic Agent**: Enforces realism.
*   **Frontline Evidence Agent**: Compacts the approved package into a structured handoff describing campaign type, objectives, constraints, and supporting metrics.

## Planner Group
Planner Group is the creative brain.
*   **Goal Planning**: Produces a campaign charter with name, theme, hero promise, action plan, measurement targets, collaboration owners, and schedule intent. Each action includes consumer-facing copy (e.g., "Spend 10K THB this month, unlock 5% cashback on 10 rides next month"), quantified KPI targets, reward logic, and contingency notes.
*   **Segmentation Discovery**: Converts that charter into executable audiences with eligibility attributes, sizes, reward mechanics, offer copy, CTA hints, frequency and spend goals.
*   **Planner Critic**: Loops until plans are feasible.
*   **Reporter**: Emits a strict JSON contract covering campaign messaging, KPI targets with baselines, schedule plan, delivery plan for eligibility/email/push, risks, and confidence.

All planner tools, including a mock `segment_group_preparing_tool`, live inside this repo.

## Delivery Group
Delivery Group behaves like a true channel pod.
*   **ParallelAgent**: Executes Eligibility, Email, and Push specialists simultaneously.
*   **Eligibility Specialist**: Documents rules, uses local tools to set eligibility, find + create audiences, and records a creation event.
*   **Email/Push Specialists**: Craft final creative (subject/body/CTA or title/body/CTA), invoke channel payload tools, and register their own creation events.
*   **Delivery Aggregator**: Gathers planner_result plus specialist outputs, reiterates KPIs, messaging, and schedule, then returns a final packet with all creation events.

## Conclusion
The result is a modular Campaign Ops engine that turns vague growth goals into specific offers like "Free Point Dash: Complete 20 wallet transactions in 30 days, earn 400 bonus points" without manual wrangling. It shows how ADK-based multi-agent systems can mirror real marketing orgs, enforce data-driven rigor, and produce persuasive consumer-ready content.
