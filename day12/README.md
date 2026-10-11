\# Day 12 — LangGraph Fundamentals and LLM-Powered Workflows



\## Overview

Built stateful workflows using LangGraph, including conditional routing and an LLM-powered change risk assessment workflow for enterprise IT change management.



\## Learning Objectives

\- Understand LangGraph, StateGraph, nodes, edges, START, and END.

\- Understand the difference between linear chains and conditional graphs.

\- Maintain workflow information using shared state.

\- Implement conditional routing based on workflow results.

\- Integrate an LLM with LangGraph.

\- Generate structured outputs using Pydantic.

\- Build a preliminary change risk assessment workflow.



\## Projects



\### 1. Simple Graph

\*\*File:\*\* `simple\_graph.py`



Created a basic graph using StateGraph, a greeting node, START, and END.



\### 2. Rule-Based Change Workflow

\*\*File:\*\* `change\_workflow.py`



Implemented a basic change management workflow that classifies changes into high, medium, and low risk using predefined rules and routes them to the appropriate review path.



\### 3. LLM-Powered Change Workflow

\*\*File:\*\* `llm\_change\_workflow.py`



Integrated LangChain's ChatOpenAI model with LangGraph.



The workflow:

1\. Accepts a change description.

2\. Uses an LLM to assess potential risk.

3\. Returns structured output using a Pydantic model.

4\. Stores the risk level and rationale in workflow state.

5\. Uses conditional edges to route high-risk changes to enhanced review and other changes to standard review.

6\. Returns the final workflow state.



\## Key Concepts

\- LangGraph and StateGraph

\- Nodes and edges

\- Conditional edges

\- Shared state

\- START and END

\- Graph compilation and invocation

\- LLM integration

\- Structured output and Pydantic

\- Agentic workflow orchestration



\## Important Design Considerations

\- LLM risk assessments are preliminary recommendations, not official approval decisions.

\- Structured output validates response structure but does not guarantee factual correctness.

\- Real-world implementations require approved risk policies, business-rule validation, appropriate human approval, and evaluation.



\## Technology Stack

\- Python

\- LangGraph

\- LangChain

\- OpenAI API

\- Pydantic

\- python-dotenv



\## Outcome

Successfully built a conditional workflow that integrates an LLM-based risk assessment with stateful graph orchestration for a practical change management use case.

