\# Day 14 — Tool-Calling Agent with LangGraph



\## Overview

Built a tool-calling agent using LangGraph, LangChain, and the OpenAI API. The application uses conditional routing to decide when to execute a Python tool and when to return a direct answer.



\## Learning Objectives

\- Integrate LLM tool calling with LangGraph.

\- Use `MessagesState` to maintain conversation messages.

\- Execute tools with `ToolNode`.

\- Route execution using `tools\_condition`.

\- Create a tool-calling loop.

\- Handle unsupported tool inputs.

\- Distinguish direct LLM responses from tool-assisted responses.



\## Project: Change Management Tool Agent



\*\*File:\*\* `langgraph\_tool\_agent.py`



\### Workflow

1\. Accept a user question.

2\. Pass conversation messages to the LLM.

3\. Route to the tool node when the LLM requests a tool.

4\. Execute the requested Python function.

5\. Return the tool result to the LLM.

6\. Repeat if another tool call is required.

7\. Finish when the LLM returns a response without requesting a tool.



\## Key Components

\- `MessagesState`

\- `StateGraph`

\- `ToolNode`

\- `tools\_condition`

\- `ChatOpenAI`

\- `bind\_tools()`

\- Conditional routing and graph loops



\## Test Scenarios

\- Normal change requirements: tool-assisted response.

\- Unsupported standard change category: controlled fallback.

\- General AI-agent question: direct response without tool execution.



\## Technology Stack

\- Python

\- LangGraph

\- LangChain

\- OpenAI API

\- python-dotenv



\## Engineering Considerations

Tool calling separates the model's decision to request an operation from the application's execution of that operation. Production implementations should validate inputs, restrict permissions, handle tool failures, limit repeated execution, and distinguish trusted policy information from general model-generated guidance.



\## Outcome

Successfully built a stateful LangGraph agent that can call a change-management requirements tool, process its result, and respond directly when tool usage is unnecessary.

