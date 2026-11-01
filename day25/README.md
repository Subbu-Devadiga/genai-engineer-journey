\# Day 25 – Hybrid Search: BM25 + Vector Search + RRF



\## Objective



Implement and evaluate hybrid retrieval by combining lexical search (BM25) and semantic vector search (ChromaDB) using Reciprocal Rank Fusion (RRF).



\## Concepts Learned



\- BM25 keyword-based retrieval.

\- Exact identifier matching in enterprise documents.

\- Semantic retrieval using embeddings.

\- Hybrid search architecture.

\- Reciprocal Rank Fusion (RRF).

\- Precision@K and Recall@K.

\- Retrieval evaluation and ranking comparison.



\## Implementation



Created a hybrid retrieval application using the existing Change Management ChromaDB collection.



Three retrieval strategies were implemented:



1\. BM25 – keyword-based document retrieval.

2\. Vector Search – semantic similarity retrieval.

3\. Hybrid Search – combines both rankings using RRF.



\### RRF Formula



RRF(d) = Σ 1 / (k + rank(d))



Used k = 60.



\## Evaluation Results



Average performance across three test queries:



| Retrieval Method | Average Precision@3 | Average Recall@3 |

|---|---:|---:|

| BM25 | 0.33 | 0.56 |

| Vector Search | 0.67 | 0.89 |

| Hybrid Search | 0.56 | 0.78 |



\## Key Observations



\- BM25 performed well for exact keyword matching.

\- Vector search performed better on the tested semantic queries.

\- Hybrid search combined rankings from both retrieval methods.

\- RRF did not outperform vector search across all test cases.

\- Combining retrieval strategies does not automatically guarantee better results.



\## Enterprise Application



For a Change Management AI assistant:



\- Use exact identifier lookup for change IDs.

\- Use BM25 for keyword-based retrieval.

\- Use vector search for semantic queries.

\- Combine retrieval results using RRF.

\- Apply metadata filters and reranking.

\- Evaluate retrieval quality before selecting a strategy.



\## Key Takeaway



Better retrieval leads to better context, which supports more grounded LLM responses.



Retrieval quality must be measured rather than assumed.



\## Technologies Used



\- Python

\- LangChain

\- ChromaDB

\- OpenAI Embeddings

\- rank-bm25

\- Reciprocal Rank Fusion



\## Files



\- `bm25\_demo.py` – standalone BM25 demonstration.

\- `hybrid\_search.py` – BM25, vector search, RRF and evaluation implementation.



\*\*Day 25 Status: Completed\*\*

