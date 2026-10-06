\# Day 10 - RAG Retrieval Optimization



\## Topics



\- Document chunking

\- Chunk size

\- Chunk overlap

\- Metadata

\- Metadata filtering

\- Top-K retrieval

\- Retrieval distance

\- Reranking

\- Hybrid search

\- Retrieval quality



\## Practical Work



\### 1. Chunking Demo



Implemented a simple chunking mechanism and experimented with:



\- Different chunk sizes

\- Different overlap values



Observed that very small chunks can fragment context while very large chunks can introduce unnecessary information.



\### 2. Metadata Demo



Implemented metadata-based filtering using:



\- Category

\- Type

\- Environment



\### 3. Improved RAG



Enhanced the Day 9 RAG application to:



\- Retrieve Top-K documents

\- Display document IDs

\- Display retrieval distances

\- Handle multiple queries

\- Ground answers using retrieved context



\### 4. Retrieval Comparison



Compared:



\- Top-K = 1

\- Top-K = 3

\- Top-K = 5



Observed the trade-off between retrieval coverage and irrelevant context.



\## Key Concepts



\### Chunking



Chunking splits large documents into smaller pieces that can be independently embedded and retrieved.



\### Chunk Overlap



Overlap preserves surrounding context between adjacent chunks.



\### Top-K



Top-K determines how many candidate documents are retrieved.



\### Reranking



Reranking performs a more detailed relevance assessment on retrieved candidates.



\### Hybrid Search



Hybrid search combines semantic/vector search with keyword-based search.



\## Production RAG Architecture



Documents

→ Chunking

→ Metadata

→ Embeddings

→ Vector/Hybrid Search

→ Top-K Candidates

→ Reranking

→ Top Relevant Chunks

→ LLM

→ Grounded Answer



\## Key Takeaway



RAG quality depends heavily on retrieval quality.



Improving the LLM alone is not enough. Chunking, embeddings,

metadata, retrieval strategy, Top-K selection and reranking

all contribute to the quality of the final answer.

