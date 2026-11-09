\# Day 30 – Building an Intelligent Enterprise RAG Workflow with LangGraph



\## Objective



Build an intelligent Enterprise Change Management RAG application using LangGraph, LangChain, OpenAI and ChromaDB.



The objective was to create a dynamic retrieval workflow that selects the most appropriate retrieval strategy based on the user's question, handles retrieval failures and generates grounded answers with source document attribution.



\## Concepts Covered



\- LangGraph StateGraph and workflow orchestration

\- LLM-based query routing

\- Conditional edges and execution paths

\- Vector similarity search

\- Metadata-based retrieval using ChromaDB

\- Multi-query retrieval

\- Reciprocal Rank Fusion (RRF)

\- Retrieval fallback mechanisms

\- Context-based answer generation

\- Source document attribution

\- Environment variable management using python-dotenv



\## Architecture



```text

&#x20;                START

&#x20;                  |

&#x20;                  v

&#x20;            Query Router

&#x20;                  |

&#x20;         Conditional Routing

&#x20;                  |

&#x20;      +-----------+-----------+

&#x20;      |           |           |

&#x20;      v           v           v

&#x20;  Vector       Metadata    Multi-Query

&#x20;  Search        Filter      Retrieval

&#x20;      |           |           |

&#x20;      |           v           |

&#x20;      |      Check Results    |

&#x20;      |           |           |

&#x20;      |      +----+----+      |

&#x20;      |      |         |      |

&#x20;      |      v         v      |

&#x20;      |   Results    No Results

&#x20;      |      |         |

&#x20;      |      |    Vector Search

&#x20;      |      |         |

&#x20;      +------+---------+

&#x20;             |

&#x20;             v

&#x20;        Answer Node

&#x20;             |

&#x20;             v

&#x20;            END

```



\## Implementation Details



\### 1. LLM-Based Query Routing



Implemented an LLM-powered router to classify incoming questions into three retrieval categories:



\- \*\*VECTOR\_SEARCH:\*\* For conceptual questions requiring semantic retrieval.

\- \*\*METADATA\_FILTER:\*\* For questions requesting specific records using metadata such as category, type or source.

\- \*\*MULTI\_QUERY:\*\* For complex or broad questions requiring alternative search queries.



\### 2. ChromaDB Integration



Connected the workflow to the existing Change Management vector database.



\- Embedding model: `text-embedding-3-small`

\- Vector database: ChromaDB

\- LLM: `gpt-6-astra`

\- Retrieval method: Similarity search



\### 3. Metadata-Based Retrieval



Implemented metadata filtering to retrieve documents based on specific attributes.



Example:



```python

{

&#x20;   "$and": \[

&#x20;       {"category": "Change Management"},

&#x20;       {"source": "emergency\_change"}

&#x20;   ]

}

```



Handled metadata retrieval failures by falling back to normal vector search when no matching documents were found.



\### 4. Multi-Query Retrieval with RRF



Implemented multi-query retrieval to improve document coverage.



Workflow:



1\. Generate alternative queries using an LLM.

2\. Perform vector similarity search for each query.

3\. Combine the individual retrieval lists.

4\. Remove duplicate documents.

5\. Apply Reciprocal Rank Fusion to rerank the documents.

6\. Pass the top-ranked documents to the answer-generation node.



RRF combines document rankings using:



\\\[

RRF(d)=\\sum\_{r \\in R}\\frac{1}{k+rank\_r(d)}

\\]



Documents appearing consistently near the top across multiple retrieval lists receive higher combined scores.



\### 5. Grounded Answer Generation



Implemented an answer-generation node using retrieved documents as context.



The prompt instructs the LLM to:



\- Answer using only retrieved context.

\- Avoid inventing unsupported information.

\- Clearly communicate when information is insufficient.

\- Generate structured and relevant responses.

\- Include supporting source document names.

\- Avoid claiming approval unless explicitly supported by the context.



\### 6. Source Attribution



The generated answers include source document references, allowing users to identify the knowledge-base documents supporting the response.



Example sources:



\- `rollback`

\- `resolution\_and\_recovery`

\- `production\_validation`

\- `post\_release\_verification`



\## Testing and Results



Tested the workflow using three different questions.



| Test Question | Selected Route | Result |

|---|---|---|

| What is the rollback procedure? | VECTOR\_SEARCH | Retrieved 5 documents and generated a grounded answer. |

| Find emergency changes related to SAP in production. | METADATA\_FILTER | Retrieved the emergency change document and identified missing SAP-specific details. |

| Compare recovery procedures for failed production deployments. | MULTI\_QUERY | Generated alternative queries, applied RRF and retrieved 5 documents for answer generation. |



\### Important Observations



\- The router successfully selected different retrieval strategies.

\- Metadata retrieval successfully returned matching documents.

\- The fallback mechanism was implemented for empty metadata results.

\- Multi-query retrieval improved the retrieval approach by considering alternative query formulations.

\- RRF combined individual rankings into a unified ranked list.

\- The answer-generation node produced structured answers with source attribution.

\- The assistant avoided inventing detailed procedures when the knowledge base did not contain sufficient information.



\## Key Learnings



1\. LangGraph provides explicit workflow orchestration through nodes, edges and shared state.

2\. Conditional routing enables dynamic retrieval based on the user's question.

3\. Multiple retrieval strategies can improve enterprise document retrieval.

4\. RRF combines rankings from multiple retrieval lists.

5\. Fallback mechanisms improve retrieval resilience.

6\. Grounded answer generation reduces unsupported responses.

7\. Source attribution improves transparency and traceability.



\## Day 30 Outcome



Successfully implemented an intelligent Enterprise RAG workflow using LangGraph, integrating dynamic query routing, ChromaDB retrieval, metadata filtering, multi-query retrieval with RRF, fallback handling and source-attributed answer generation.



\*\*Next:\*\* Day 31 – RAG Reliability, Hall

