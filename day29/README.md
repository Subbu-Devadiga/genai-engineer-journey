\# Day 29 – Advanced RAG: Query Routing and Self-Query Retrieval



\## Objective

Implement intelligent query routing and metadata-aware retrieval for an enterprise Change Management RAG assistant.



\## Concepts Covered

\- LLM-based query routing

\- Vector search routing

\- Metadata filter routing

\- Query intent classification

\- Self-query retrieval

\- Structured metadata extraction

\- ChromaDB metadata filtering

\- Combining multiple metadata conditions using `$and`



\## Implementation



Created the following Python scripts:



\- `query\_router.py` – Classifies user questions into retrieval strategies.

\- `inspect\_metadata.py` – Inspects available metadata fields in ChromaDB.

\- `self\_query\_retrieval.py` – Extracts metadata filters from natural-language questions and applies them during retrieval.



\## Query Routing Categories



| Route | Purpose |

|---|---|

| VECTOR\_SEARCH | Retrieves semantically relevant documents |

| METADATA\_FILTER | Retrieves documents using structured metadata |

| MULTI\_QUERY | Expands complex questions into multiple retrieval queries |



\## Metadata Schema



The existing ChromaDB collection contains:



\- `category`

\- `type`

\- `source`



\## Practical Tests



\### Test 1 – Change Management



Question: Find all Change Management procedures.



Extracted conditions:

\- category = Change Management

\- type = Procedure



Successfully retrieved five matching documents, including normal changes, CAB, emergency changes, production validation and change closure.



\### Test 2 – Release Management



Question: Find all Release Management procedures.



Extracted conditions:

\- category = Release Management

\- type = Procedure



Successfully retrieved five matching documents, including release planning, staging and UAT, build and packaging, deployment strategy and release cutover.



\## Key Learnings



1\. Query routing selects an appropriate retrieval strategy based on user intent.

2\. Self-query retrieval translates natural-language requirements into structured metadata filters.

3\. Metadata filtering improves retrieval precision for structured queries.

4\. ChromaDB supports multiple filter conditions through operators such as `$and` and `$or`.

5\. LLM-generated filters should be validated before execution.

6\. Metadata filtering and vector similarity search can work together.



\## Practical Application



Implemented metadata-aware retrieval for an enterprise Change Management knowledge assistant, allowing users to retrieve procedures from specific knowledge categories using natural-language questions.



\## Future Improvements



\- Integrate routing and retrieval into one workflow.

\- Add metadata schema and value validation.

\- Explore LangChain's dedicated SelfQueryRetriever.

\- Add a fallback for unsupported or missing metadata.

\- Evaluate routing accuracy, retrieval quality and latency.

