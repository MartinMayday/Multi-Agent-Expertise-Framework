---

source-video: https://www.youtube.com/watch?v=zTcDwqopvKE

---

# Agent Expert - Framework draft

"Self-Improving Template Meta Prompt"
    Meta Prompt: A prompt that builds other prompts. Template: Focused on solving a specific, recurring problem. Self-Improving: Automatically updates itself, related prompts, or isolated files with new information that improves your agent's next execution.

## The Expert's Mental Model - Topic Focus
- Information
- Examples
- Paterns
- Expertise

---

# meta_prompt.md
---
allowed-tools: Write, Edit, WebFetch, Task, mcp__firecrawl-mcp__firecrawl_scrape, Fetch
description: Create a new prompt based on a user's request
---

# Purpose

This meta prompt takes the `USER_PROMPT_REQUEST` and follows the `workflow` to create a new prompt in the `Specified Format`.

## Variables


## Instructions


## Workflow


## Specified Format


Use example:
/meta_prompt create a new version of .claude/commands/question.md called question-w-mermaid-diagrams.md where we add diagrams to the answer to the question

---

# meta-agent.md
---
name: meta-agent
description: Create a new prompt based on a user's request
tools: Write, WebFetch, mcp__firecrawl-mcp__firecrawl_scrape, mcp__firecrawl-mcp__firecrawl_search, MultiEdit
color: cyan
model: opus
---

# Purpose

You are a meta-agent generator. An agent that generates other agents. You take a user's prompt describing a new sub-agent and generate a complete, ready-to-use sub-agent configuration file. You then write this file to `.claude/agents/<name>.md`.


## Instructions


## Workflow


## Output format


Use example:
@agent-meta-agent create a planner agent that directly reads and executes the .claude/commands/plan.md prompt. Simple and concise. Pass the incoming prompt through to the plan using the SlashCommand tool.

---

### SKILL.md
---
name: creating-new-skills
description: Creates new Agent Skills for AI Agents following best practices and documentation. USE WHEN the user wants prompts 'create a new skill...' or 'use your meta skill to...'.
---

# Purpose

Create new Agent Skills for AI Agents by following a structured workflow based on best practices and comprehensive documentation.


## Instructions


## Examples


## Summary


Use example:
use the meta-skill: create 'start-orchestrator' skill that kicks off our frontend and backend of apps/orchestrator_3_stream/application in background mode by default (adjustable). it will know how to kick off the backend with specific params, make sure it reads the scripts/start_fe.sh and scripts/start_be.sh so its aware of flags (session + cwd) after the apps are running, open the ui in chrome

---