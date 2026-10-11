\# Day 13 — LLM Tool Calling



\## Overview

Built a tool-calling application using Python, LangChain, and the OpenAI API. The application enables an LLM to request a predefined Python function to retrieve IT change-management requirements.



\## Learning Objectives

\- Understand LLM tool calling.

\- Define Python functions as tools using `@tool`.

\- Register tools using `bind\_tools()`.

\- Inspect tool calls returned by the model.

\- Execute tools in application code.

\- Return tool results using `ToolMessage`.

\- Generate final responses using tool results.

\- Handle unsupported tool arguments safely.



\## Project: Change Management Requirements Assistant



\*\*File:\*\* `tool\_calling.py`



\### Workflow

1\. Receive a user question about change documentation.

2\. Provide the model with available tool definitions.

3\. Let the model request the relevant tool.

4\. Execute the Python function with the supplied arguments.

5\. Return the tool result to the model.

6\. Generate a final response based on the retrieved information.



\### Supported Categories

\- Normal changes

\- Emergency changes



Unsupported categories return a controlled fallback message.



\## Key Concepts

\- LLM tool calling

\- LangChain `@tool`

\- `bind\_tools()`

\- `response.tool\_calls`

\- Tool execution and argument validation

\- `ToolMessage`

\- Tool-calling loops

\- Least-privilege access and safe fallbacks



\## Test Scenarios

\- Emergency change requirements

\- Normal change requirements

\- Unsupported standard change category



\## Technology Stack

\- Python

\- LangChain

\- OpenAI API

\- Pydantic-compatible tool schemas

\- python-dotenv



\## Security Considerations

The model requests tool calls, but application code controls execution. Production systems should validate arguments, enforce authorization, restrict tool access, log sensitive operations, and avoid presenting unverified general guidance as official policy.



\## Outcome

Successfully implemented an LLM tool-calling workflow that retrieves predefined change-management requirements and uses the results to formulate a response.

