\# Day 26 – Cross-Encoder Reranking



\## Objective



Understand and implement Cross-Encoder reranking to improve document relevance in a Retrieval-Augmented Generation (RAG) pipeline.



\## Concepts Learned



\- Bi-Encoder vs Cross-Encoder architecture.

\- Semantic retrieval using embeddings.

\- Cross-Encoder relevance scoring.

\- Query-document pair scoring.

\- Two-stage retrieval architecture.

\- Candidate retrieval size and recall.

\- Precision@K and Recall@K evaluation.

\- Retrieval latency and computational trade-offs.



\## Implementation



Implemented a standalone Cross-Encoder demonstration using:



`cross-encoder/ms-marco-MiniLM-L-6-v2`



Integrated Cross-Encoder reranking with the existing ChromaDB Change Management knowledge base.



\### Retrieval Pipeline



1\. Retrieve candidate documents using ChromaDB vector search.

2\. Create query-document pairs.

3\. Calculate relevance scores using Cross-Encoder.

4\. Sort documents based on relevance scores.

5\. Select the final top 3 documents.



\## Candidate Size Experiment



Tested two candidate retrieval sizes for the query:



"How do I recover after a failed deployment?"



| Candidate Size | Initial Precision@3 | Reranked Precision@3 | Reranked Recall@3 |

|---|---:|---:|---:|

| Top 5 | 0.33 | 0.67 | 0.67 |

| Top 10 | 0.33 | 1.00 | 1.00 |



\## Key Observations



\- Cross-Encoder moved relevant documents higher in the ranking.

\- Increasing candidate retrieval size allowed the rollback document to enter the candidate pool.

\- Cross-Encoder cannot retrieve documents missing from the initial candidate set.

\- Larger candidate pools increase reranking computation and latency.

\- Relevance scores are ranking signals, not probabilities.

\- Reranking performance must be evaluated using relevance judgments.



\## Enterprise Application



For a Change Management AI assistant:



\- Retrieve candidate documents using vector or hybrid search.

\- Rerank candidates using Cross-Encoder.

\- Prioritize rollback, recovery and incident-resolution documents when relevant.

\- Pass the most relevant documents to the LLM.

\- Evaluate retrieval quality, latency and cost.



\## Technologies Used



\- Python

\- Sentence Transformers

\- Hugging Face

\- Cross-Encoder

\- ChromaDB

\- LangChain

\- OpenAI Embeddings



\## Key Takeaway



Bi-Encoder retrieves candidate documents efficiently, while Cross-Encoder performs more detailed query-document relevance scoring to improve their ranking.



A reliable RAG pipeline requires both good candidate retrieval and effective reranking.



\*\*Day 26 Status: Completed\*\*

