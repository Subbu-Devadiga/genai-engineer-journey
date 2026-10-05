\# Day 09 - End-to-End RAG Application



\## Topics



\- Retrieval-Augmented Generation

\- Query embeddings

\- Vector search

\- Context retrieval

\- LLM generation

\- Grounded responses

\- Source attribution

\- RAG failure modes



\## Practical Work



Built an end-to-end RAG application using:



\- OpenAI embeddings

\- ChromaDB

\- OpenAI Responses API

\- Change-management knowledge base



\## Architecture



User Question

→ Query Embedding

→ ChromaDB

→ Relevant Documents

→ Context

→ LLM

→ Grounded Answer



\## Key Takeaway



RAG combines information retrieval with LLM generation.

The retrieval system provides relevant external knowledge,

while the LLM uses that context to generate a grounded answer.

























What is RAG?

Retrieval Augmented generation-Retrieves relevant external information provides it as a context to llm so the model can generate an answer grounded in that retrieved information.



Why do we need RAG if LLMs already know a lot of information?

While Large Language Models (LLMs) possess vast general knowledge, they lack access to proprietary, private, or real-time data that organizations and individuals cannot—or prefer not to—share publicly. This is where Retrieval-Augmented Generation (RAG) comes in. RAG queries an external, secure knowledge base to retrieve only the relevant information needed for a user's prompt, injecting that data into the LLM as focused context to generate accurate, tailored responses



Explain the complete RAG pipeline.

Step1:User asks a query

Step2:Convert question to embedding, where embedding model converts question into query vector.

Step3:Search chromadb. Based on query vector performs a similarity search and retrieve top 3 relevant documents.

Step4:Build context, Combine all the retrieved documents

Step5:Send context and user query as a prompt to LLM.

Step6: LLMs processes prompts to produce accurate and tailored answer based on context.



What is the role of the embedding model in RAG?

Role of embedding model is numerical vector representation of the text or user query.



What is the role of the LLM in RAG?

Role of LLM is to process and produce accurate, tailored responses based on context and user query provided.



Why do we convert the user query into an embedding?

We convert query into embedding to capture it's semantic meaning and contextual relationship.



Why do we retrieve multiple documents instead of just one?

Because some times user questions requires information that is spread across multiple documents. 



What is top-k retrieval?

Top-k retrieval is scoring the documents or data chunks and returning the top k highest scoring results for a given query



What is a context window?

Context window is maximum number of tokens than a LLM can process, remember and respond to in a single operations.



What happens if the relevant document isn't retrieved?

If the relevant documents are not retrieved then it may reduce answer quality and may cause the llm to produce inaccurate, unsupported or irrelevant response.



What happens if irrelevant documents are retrieved?

It may reduce answer quality and may cause the llm to produce inaccurate, unsupported or irrelevant response.



What is a RAG hallucination?

RAG hallucination is an error where llm model misunderstands retrieved context and produces false, unsupported information even though it has relevant context.



Why should RAG applications provide source information?

RAG Applications should provide source information to build user trust, to verify the facts and for troubleshooting.





What is the difference between retrieval and generation?

Retrieval is process of finding and extracting relevant information from an external database.

Generation is LLMs produce response based on the context and user query.





Explain this:

Question

&#x20;  ↓

Embedding

&#x20;  ↓

Vector Search

&#x20;  ↓

Retrieved Context

&#x20;  ↓

Prompt

&#x20;  ↓

LLM

&#x20;  ↓

Answer



Explain the complete RAG pipeline.

When User asks a question, it will be converted to vector representation, where embedding model converts question into query vector. Then based on query vector performs a similarity search in vector database and retrieves top k relevant documents. Then all the retrieved documents will be combined together to build a context. Once the context is built it will be combined with the question and will be sent as a prompt to LLM. Then LLM model processes it and produces an accurate and tailored answer based on context and user query.



&#x20;— Interview challenge

Suppose your RAG system has 1 million document chunks, but the correct chunk isn't appearing in the top 5 results.

What could be wrong, and how could you improve the system?

What could be wrong : Less efficient embedding model, poor chunking , vocabulary mismatch

We can improve it by finetuning embedding model accuracy.









