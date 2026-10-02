\# Day 08 - Embeddings \& Vector Search



\## Topics



\- Embeddings

\- Semantic search

\- Cosine similarity

\- Vector databases

\- ChromaDB

\- Metadata

\- Retrieval

\- RAG fundamentals



\## Practical Work



\- Generated OpenAI embeddings

\- Built semantic search using NumPy

\- Stored embeddings in ChromaDB

\- Queried the vector database

\- Added metadata

\- Tested enterprise change-management queries

\- Expanded the knowledge base



\## Key Takeaway



Embeddings convert text into numerical representations that can

be compared for semantic similarity. Vector databases provide

efficient storage and retrieval of these representations.

This retrieval capability forms the foundation of RAG systems.









What is an embedding?

An embedding is a numerical representation of text that captures semantic relationship between pieces of text or tokens.



Why are embeddings useful for semantic search?

Embedding vectors of words having similar semantic meaning will point in similar direction so their cosine similarity score will be higher. In this way embeddings are useful for semantic search.



What is a vector database?

vector database stores vectors and efficiently allows us to search for vectors that are similar to query vector.



Why can't we simply use keyword search for every knowledge-retrieval problem?

The documents might not have the exact keywords that we are used in our query. Document we are searching might contain different words that has similar meaning. In such cases key word searches are not useful.



What is cosine similarity?

Measures how similar two vectors are by comparing angle between them. A higher cosine similarity generally indicates that vectors point in more similar direction.



What does a vector database store?

Vector data base stores ID, vector, Text document chunks, metadata.



Why do we need a vector database instead of a Python list when the dataset becomes large?

Python list is useful for small number of dataset but when dataset becomes larger python list is not efficient because it has to traverse through everything each time when we search for something. But vector database provides capabilities such as vector storage, similarity search, metadata filtering, indexing, persistence and scalability. 



What is semantic search?

Semantic search is identifying words that has similar meaning. Similar meanings tend to produce vectors that are closer according to the chosen similarity/distance measure.



What is the difference between keyword search and semantic search?

Keyword search is to find the data that matches exact keywords.

Semantic search is finding the words that has similar meanings, may not be exact words through embedding vector values.



What is RAG at a high level?

Retrieval-Augmented generation(RAG) is a technique to improve llm model's answer by searching an external knowledge base before it replies.



Is a vector database itself an LLM?

No, vector database itself is not an LLM. Vector database stores vector/data from external knowledge base that is required for llm model to answer user query.



Why do we need to convert the user query into an embedding during semantic search?

Models cannot process texts, they process numbers. Through embedding user query will be numerically represented. To calculate cosine similarity it is important to convert user query to embedding. Cosine similarity is used in semantic search



Why should documents contain metadata?

In large enterprise RAG systems metadata is extremely useful for filtering documents.



What happens if we retrieve irrelevant documents and pass them to an LLM?

LLM models will produce incorrect outputs.



Explain this architecture:

Documents

&#x20;  ↓

Embeddings

&#x20;  ↓

Vector Database

&#x20;  ↓

User Query

&#x20;  ↓

Query Embedding

&#x20;  ↓

Similarity Search

&#x20;  ↓

Relevant Documents



All the documents will be passed to embedding model and it will be converted to vectors. embedding model uses semantic search where the vectors having similar meaning points in more similar direction. Then the vectors will be stored in vector database. Then the user query will be passed to embedding model and will be converted to vectors. Then the model will search in vector database through cosine similarity scores. then model retrieves all the relevant documents where cosine similarity scores are higher.







