\# Day 15 — Agent State and Conversation Memory



\## Overview

Built a conversational change-management agent using LangGraph, an LLM, and a Python tool. Added checkpointing to preserve conversation state across multiple interactions within the same thread.



\## Learning Objectives

\- Understand graph state and conversation history.

\- Use `MessagesState` to manage messages.

\- Configure checkpointing with `InMemorySaver`.

\- Continue a conversation using the same thread ID.

\- Inspect saved state with `graph.get\_state()`.

\- Separate conversations using different thread IDs.

\- Understand the limitations of in-memory persistence.



\## Project: Conversational Change Management Agent



\*\*File:\*\* `agent\_memory.py`



\### Workflow

1\. Accept a question about change-management requirements.

2\. Retrieve relevant requirements using a Python tool.

3\. Return the tool result to the LLM.

4\. Continue the conversation using the same thread ID.

5\. Inspect the saved conversation state.

6\. Start a separate conversation using another thread ID.



\## Key Concepts

\- `MessagesState`

\- `InMemorySaver`

\- Checkpointing

\- `thread\_id`

\- `graph.get\_state()`

\- Multi-turn conversations

\- Conversation isolation

\- Short-term state versus long-term memory



\## Test Scenarios

\- Retrieve emergency-change requirements.

\- Ask a follow-up question about normal changes.

\- Inspect the saved conversation messages.

\- Start a separate conversation and verify that earlier context is not inherited.



\## Technology Stack

\- Python

\- LangGraph

\- LangChain

\- OpenAI API

\- python-dotenv



\## Limitations and Production Considerations

`InMemorySaver` is suitable for local experimentation. Its checkpoints are lost when the Python process exits. Production systems require appropriate persistent checkpoint storage, access controls, retention policies, and careful handling of sensitive conversation data.



A checkpoint preserves graph state; it is not automatically the same as a long-term memory system that retrieves selected facts across unrelated conversations.



\## Outcome

Successfully implemented a stateful agent that can continue multi-turn conversations within a thread and isolate separate conversations using different thread IDs.

