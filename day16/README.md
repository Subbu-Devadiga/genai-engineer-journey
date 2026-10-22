\# Day 16 — Persistent Memory with SQLite



\## Overview

Built a conversational change-management agent using LangGraph and SQLite checkpointing. The agent can resume a conversation after the Python process exits by loading saved graph state from a local SQLite database.



\## Learning Objectives

\- Understand the limitations of in-memory checkpointing.

\- Configure persistent checkpoints using `SqliteSaver`.

\- Resume conversations after application restarts.

\- Use `thread\_id` to identify conversations.

\- Inspect and retain graph state across invocations.

\- Understand production database and security considerations.



\## Project: Persistent Change Management Agent



\*\*File:\*\* `persistent\_agent.py`



\### Workflow

1\. Receive a change-management question.

2\. Retrieve documentation requirements using a Python tool.

3\. Return the result to the LLM for a final answer.

4\. Save the graph state in a SQLite database.

5\. Restart the application.

6\. Continue the conversation using the same database file and thread ID.



\## Key Components

\- `SqliteSaver`

\- `StateGraph`

\- `MessagesState`

\- `ToolNode`

\- `tools\_condition`

\- `thread\_id`

\- SQLite checkpoint storage



\## Test Results

\- Retrieved emergency-change documentation requirements.

\- Restarted the Python application.

\- Asked a follow-up question about normal changes.

\- Successfully continued the conversation with previously saved state.

\- Observed the message count increase from 7 to 11.



\## Technology Stack

\- Python

\- LangGraph

\- LangChain

\- OpenAI API

\- SQLite

\- python-dotenv



\## Security and Production Considerations

Conversation history can contain sensitive information. Production systems should enforce authorization and thread isolation, apply appropriate retention and deletion policies, protect stored data, and avoid logging or exposing secrets.



SQLite is useful for local learning and small applications. Multi-user deployments may benefit from a managed PostgreSQL database and persistent checkpointing configured for the chosen deployment architecture.



\## Important Distinction

A checkpointer saves graph execution state and conversation messages. It does not automatically create a separate intelligent long-term memory system that extracts useful facts across unrelated conversations.



\## Outcome

Successfully implemented persistent LangGraph checkpointing and verified that conversation state survives application restarts.

