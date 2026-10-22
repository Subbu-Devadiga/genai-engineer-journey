\# Day 17 — Long-Term Memory for GenAI Agents



\## Overview

Implemented a basic long-term memory store using LangGraph's `InMemoryStore`. The project demonstrates saving selected facts, retrieving individual memories, and isolating memory records using namespaces.



\## Learning Objectives

\- Understand the difference between checkpointing and long-term memory.

\- Store and retrieve selected facts using the LangGraph Store API.

\- Use namespaces to organize user-specific memory.

\- Retrieve only the information needed for a request.

\- Understand memory selection, privacy, and access-control considerations.



\## Project: Change Management Memory Store



\*\*File:\*\* `long\_term\_memory.py`



\### Features

\- Stores an environment and application preference.

\- Stores a response-style preference.

\- Stores an answer-format preference.

\- Retrieves individual memory records by key.

\- Lists memories within a namespace.

\- Demonstrates isolation between two user namespaces.



\## Key Concepts

\- `InMemoryStore`

\- `store.put()`

\- `store.get()`

\- `store.search()`

\- Namespaces

\- Selective retrieval

\- User isolation

\- Long-term memory design



\## Technology Stack

\- Python

\- LangGraph

\- In-memory key-value store



\## Limitations

`InMemoryStore` is intended for learning and experimentation in this project. Its contents do not survive a Python process restart. A production implementation requires an appropriate persistent store, authenticated user identities, access controls, and data-retention policies.



Namespaces organize data but do not replace application-level authorization.



\## Outcome

Successfully implemented memory storage and retrieval, demonstrated user namespace isolation, and explored how selected facts can support future interactions without loading an entire conversation history.

