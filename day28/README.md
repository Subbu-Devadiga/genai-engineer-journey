\# Day 28 – Advanced RAG: Query Transformation and Multi-Query Retrieval



\## Objective

Improve RAG retrieval coverage by generating alternative search queries and combining multiple ranked retrieval results using Reciprocal Rank Fusion (RRF).



\## Concepts Covered

\- Query transformation

\- Query rewriting

\- Query expansion

\- Multi-query retrieval

\- ChromaDB vector retrieval

\- Duplicate document removal

\- Reciprocal Rank Fusion (RRF)

\- Retrieval strategy comparison



\## Implementation



Created `multi\_query\_retrieval.py`.



The implementation:

1\. Accepts an original user question.

2\. Uses an LLM to generate three alternative search queries.

3\. Searches the existing ChromaDB knowledge base using the original and generated queries.

4\. Retrieves the top five documents for each query.

5\. Combines the retrieved results.

6\. Removes duplicate content.

7\. Applies Reciprocal Rank Fusion to produce a combined ranking.

8\. Compares single-query, multi-query and RRF retrieval results.



\## Existing Technology Stack

\- Python

\- LangChain

\- OpenAI GPT-6 Astra

\- OpenAI text-embedding-3-small

\- ChromaDB



\## Practical Experiment



Original question:



"How do I recover after a failed production deployment?"



Generated alternative queries explored:

\- Rollback procedures

\- Production service restoration

\- Deployment recovery and remediation



The experiment demonstrated that alternative queries can retrieve additional relevant documents that may not appear in the original query's results.



\## Retrieval Comparison



Three approaches were examined:



1\. Single-query vector similarity search.

2\. Multi-query retrieval with duplicate removal.

3\. Multi-query retrieval with Reciprocal Rank Fusion.



RRF introduced the rollback document into the top-five ranking, demonstrating how combining rankings can change retrieval results.



\## Key Learnings



\- Vector search can miss relevant documents because of differences in terminology and query wording.

\- Multi-query retrieval explores multiple ways of expressing the same intent.

\- Simple merging and deduplication do not preserve individual retrieval rankings.

\- RRF combines multiple ranked lists using reciprocal rank scores.

\- Documents consistently appearing near the top of multiple retrieval lists receive higher combined scores.

\- RRF improves ranking aggregation but does not guarantee semantic relevance.

\- Multi-query retrieval increases API usage, retrieval operations and latency.



\## Practical Application



Implemented an advanced retrieval strategy for an enterprise Change Management knowledge base to improve discovery of rollback, recovery, deployment and production validation procedures.



\## Future Improvements

\- Compare retrieval strategies using a larger, validated evaluation dataset.

\- Evaluate Precision@K and Recall@K consistently.

\- Integrate multi-query retrieval with cross-encoder reranking.

\- Measure latency and API costs.

\- Explore query complexity-based routing between normal and advanced retrieval.

