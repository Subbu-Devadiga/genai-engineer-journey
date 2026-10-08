\# Day 11 — LangChain and Source-Aware RAG



\## Overview



Day 11 focused on learning LangChain as an orchestration framework for building LLM applications and rebuilding the RAG application developed earlier using LangChain.



The main goal was to understand the abstractions provided by LangChain rather than treating the framework as a black box.



The implementation covers:



\- LangChain fundamentals

\- Chat models

\- Prompt templates

\- Output parsers

\- LCEL (LangChain Expression Language)

\- Runnables

\- RunnablePassthrough

\- RunnableLambda

\- RunnableParallel

\- ChromaDB retrievers

\- LangChain-based RAG

\- Document metadata

\- Source-aware responses

\- Grounded responses and abstention



\---



\## Learning Objectives



By the end of Day 11, I learned:



1\. What LangChain is and why it is used.

2\. How LangChain differs from directly using the OpenAI SDK.

3\. How to use `ChatOpenAI`.

4\. How to create reusable prompt templates.

5\. How LCEL connects components using the `|` operator.

6\. What a Runnable is.

7\. How output parsers work.

8\. How to convert a vector store into a retriever.

9\. How to build RAG using LangChain.

10\. How metadata can provide source traceability.

11\. How to return both an answer and retrieved sources.

12\. How to prevent the LLM from answering when the knowledge base does not contain sufficient information.



\---



\# 1. What is LangChain?



LangChain is a framework for building applications powered by language models.



It provides reusable abstractions for:



\- Chat models

\- Prompt templates

\- Retrievers

\- Vector stores

\- Tools

\- Output parsers

\- Runnables

\- Chains

\- Agents

\- Structured workflows



LangChain is not an LLM.



It acts as an orchestration layer between application logic and components such as LLMs, retrievers, tools, and data sources.



\---



\# 2. LangChain vs OpenAI SDK



For simple LLM applications, directly using the OpenAI SDK can be simpler and easier to maintain.



LangChain becomes more useful when applications grow to include:



\- Retrieval

\- Multiple model providers

\- Vector databases

\- Tools

\- Structured workflows

\- Agents

\- Reusable components

\- Complex chains



The goal is not to use LangChain everywhere, but to use it where its abstractions provide real engineering value.



\---



\# 3. Basic LangChain Application



File:



```text

basic\_langchain.py

from dotenv import load\_dotenv

from langchain\_openai import ChatOpenAI



load\_dotenv()



model = ChatOpenAI(

&#x20;   model="gpt-6-astra"

)



response = model.invoke(

&#x20;   "Explain what an emergency change is in IT change management."

)



print(response.content)







Important difference

Direct OpenAI SDK:

response.output\_text





LangChain Chat Model:

response.content





The LangChain chat model returns an AIMessage.

4\. Prompt Templates

File:

prompt\_chain.py



A prompt template creates a reusable structure for interacting with an LLM.

Example:

prompt = ChatPromptTemplate.from\_messages(    \[        (            "system",            "You are an enterprise IT Change Management assistant."        ),        (            "human",            "Explain the following change type: {change\_type}"        )    ])





The {change\_type} value can be supplied dynamically.

Example:

chain = prompt | modelresponse = chain.invoke(    {        "change\_type": "Emergency Change"    })





5\. LCEL

LCEL stands for:

LangChain Expression Language

It provides a declarative way to compose LangChain components into pipelines.

Example:

chain = prompt | model | parser





The pipeline means:

Input

&#x20; ↓

Prompt

&#x20; ↓

Model

&#x20; ↓

Output Parser

&#x20; ↓

Final Output



The | operator passes the output of one Runnable to the next Runnable.

6\. Runnables

A Runnable is a standard LangChain interface for executable and composable components.

Runnables allow different components to participate in a common execution and composition model.

Examples used in this project:

RunnablePassthroughRunnableLambdaRunnableParallel





7\. RunnablePassthrough

RunnablePassthrough() passes the original input through unchanged.

In the RAG application:

"question": RunnablePassthrough()





allows the original user question to continue through the chain while the same question is also sent to the retriever.

Conceptually:

&#x20;                   User Question

&#x20;                        |

&#x20;             +----------+----------+

&#x20;             |                     |

&#x20;             v                     v

&#x20;        Retriever            Passthrough

&#x20;             |                     |

&#x20;             v                     v

&#x20;        Retrieved Docs           Question



8\. RunnableLambda

RunnableLambda allows a normal Python function to participate in a LangChain Runnable pipeline.

Example:

def format\_docs(docs):    return "\\n\\n".join(        doc.page\_content for doc in docs    )





It can be converted into a Runnable:

format\_docs\_runnable = RunnableLambda(format\_docs)





This allows the function to participate in LCEL composition.

9\. RunnableParallel

RunnableParallel allows multiple independent branches to process the same input and return multiple outputs.

In the source-aware RAG application:

RunnableParallel(    answer=answer\_chain,    sources=RunnableLambda(        lambda x: format\_sources(x\["docs"])    ))





The application produces:

Retrieved Documents

&#x20;       |

&#x20;  +----+----+

&#x20;  |         |

&#x20;  v         v

&#x20;Answer    Sources

&#x20;  |         |

&#x20;  +----+----+

&#x20;       |

&#x20;       v

Final Result



The final result contains:

{    "answer": "...",    "sources": "..."}





10\. LangChain RAG Architecture

The RAG application connects the concepts learned on previous days with LangChain.

Architecture:

User Question

&#x20;     |

&#x20;     v

&#x20;  Retriever

&#x20;     |

&#x20;     v

&#x20;  ChromaDB

&#x20;     |

&#x20;     v

Retrieved Documents

&#x20;     |

&#x20;     +------------------+

&#x20;     |                  |

&#x20;     v                  v

&#x20;Format Context      Extract Sources

&#x20;     |                  |

&#x20;     v                  |

&#x20;Prompt Template         |

&#x20;     |                  |

&#x20;     v                  |

&#x20;ChatOpenAI              |

&#x20;     |                  |

&#x20;     v                  |

&#x20;Output Parser           |

&#x20;     |                  |

&#x20;     +--------+---------+

&#x20;              |

&#x20;              v

&#x20;        Answer + Sources



11\. Vector Store and Retriever

The existing ChromaDB knowledge base from Day 8 was reused.

vectorstore = Chroma(    collection\_name="change\_management",    embedding\_function=embeddings,    persist\_directory="../day08/chroma\_db")





The vector store was converted into a retriever:

retriever = vectorstore.as\_retriever(    search\_kwargs={"k": 3})





The retriever:

1\. Receives the user query.

2\. Searches the underlying vector store.

3\. Retrieves relevant documents.

4\. Returns LangChain Document objects.

A Document contains:

Document

├── page\_content

└── metadata



12\. Document Metadata

Metadata was added to the existing knowledge base to support traceability.

Example:

{    "category": "Change Management",    "type": "Procedure",    "source": "production\_validation"}





The metadata allows the application to identify where retrieved information came from.

Example output:

Sources:

\- production\_validation

\- staging\_and\_uat

\- normal\_change



This is important for enterprise applications because users should be able to verify the information supporting an AI-generated answer.

13\. Source-Aware RAG

The final application returns both:

Answer

Sources



Example:

Answer:



Before implementing a production change, confirm risk and impact,

implementation steps, validation activities, and rollback procedures.



Sources:

\- production\_validation

\- staging\_and\_uat

\- normal\_change



This improves:

\- Traceability

\- Auditability

\- User trust

\- Troubleshooting

\- Verification of AI responses

14\. Grounded Response / Abstention

The application was designed to avoid inventing information that is not available in the knowledge base.

The prompt instructs the LLM:

Answer the question using ONLY the provided context.



If the answer is not available in the context, say:

"The provided knowledge base does not contain enough information."



For example:

Question:

What is the maximum number of CAB members required for a change?



The knowledge base does not contain that information.

The application returns:

The provided knowledge base does not contain enough information.



This demonstrates a basic grounding/abstention mechanism.

15\. Important LangChain Components

Component	Purpose

ChatOpenAI	Connects LangChain to the OpenAI chat model

ChatPromptTemplate	Creates reusable prompts

StrOutputParser	Converts model output into a string

RunnablePassthrough	Passes input through unchanged

RunnableLambda	Wraps a Python function as a Runnable

RunnableParallel	Runs multiple branches and returns multiple outputs

Chroma	Vector store integration

Retriever	Retrieves relevant documents

Document	Represents retrieved content and metadata





16\. Manual RAG vs LangChain RAG

Manual RAG

Question

&#x20;  ↓

Create Query Embedding

&#x20;  ↓

ChromaDB Query

&#x20;  ↓

Retrieve Documents

&#x20;  ↓

Build Context

&#x20;  ↓

Create Prompt

&#x20;  ↓

OpenAI API

&#x20;  ↓

Extract Answer



LangChain RAG

Question

&#x20;  ↓

Retriever

&#x20;  ↓

Chroma

&#x20;  ↓

Document Objects

&#x20;  ↓

Prompt Template

&#x20;  ↓

ChatOpenAI

&#x20;  ↓

Output Parser

&#x20;  ↓

Answer



LangChain does not change the fundamental RAG architecture.

It provides abstractions for composing and orchestrating the components.

17\. Why Learn Manual RAG Before LangChain?

Building RAG manually before using LangChain provides several advantages:

1\. Understand the underlying RAG architecture.

2\. Understand what each LangChain abstraction is doing.

3\. Avoid treating LangChain as a black box.

4\. Make debugging easier.

5\. Understand when LangChain adds real value.

6\. Build the same system with or without a framework.

This provides a stronger engineering foundation than learning only the framework APIs.

18\. Enterprise RAG Considerations

A production RAG system should consider:

\- Chunking strategy

\- Embedding model

\- Metadata

\- Metadata filtering

\- Top-K retrieval

\- Hybrid search

\- Reranking

\- Similarity thresholds

\- Retrieval evaluation

\- Recall@K

\- Groundedness

\- Source attribution

\- Prompt injection protection

\- Access control

\- Observability

\- Latency

\- Cost

For a large enterprise knowledge base, a possible architecture is:

Documents

&#x20;   ↓

Chunking

&#x20;   ↓

Metadata

&#x20;   ↓

Embeddings

&#x20;   ↓

Vector / Hybrid Index

&#x20;   ↓

Metadata Filtering

&#x20;   ↓

Top 20–50 Candidates

&#x20;   ↓

Reranking

&#x20;   ↓

Top 3–5 Chunks

&#x20;   ↓

LLM

&#x20;   ↓

Grounded Answer + Sources



19\. Key Interview Questions

What is LangChain?

LangChain is a framework for building applications powered by language models. It provides abstractions for models, prompts, retrieval, tools, output parsing, and workflow composition.

Is LangChain an LLM?

No. LangChain is an orchestration framework.

Why use LangChain instead of the OpenAI SDK?

For simple applications, the OpenAI SDK can be simpler. LangChain becomes useful when applications grow to include retrieval, multiple model providers, tools, structured workflows, agents, and reusable components.

What is LCEL?

LCEL stands for LangChain Expression Language. It provides a declarative way to compose LangChain Runnables using operators such as |.

What is a Runnable?

A Runnable is a standard interface for executable and composable LangChain components.

What does prompt | model mean?

The output of the prompt Runnable becomes the input to the model Runnable.

What does a retriever return?

A retriever returns relevant LangChain Document objects from the underlying knowledge source.

What does a Document contain?

A Document generally contains:

page\_content

metadata



What does an output parser do?

An output parser converts raw model output into a format that the application can reliably use, such as a string or structured object.

Why add source metadata?

Source metadata provides traceability and allows users to verify where retrieved information came from.

20\. Day 11 Outcome

By completing Day 11, I can now:

\- Build basic LangChain applications.

\- Create reusable prompt templates.

\- Compose components using LCEL.

\- Work with LangChain Runnables.

\- Connect LangChain to OpenAI models.

\- Connect LangChain to ChromaDB.

\- Build a RAG pipeline using a retriever.

\- Work with LangChain Document objects.

\- Use metadata for source traceability.

\- Return answers with retrieved sources.

\- Implement basic grounding and abstention.

\- Explain the difference between manual RAG and LangChain RAG.

Technology Stack

\- Python

\- LangChain

\- LangChain OpenAI

\- LangChain Chroma

\- OpenAI API

\- text-embedding-3-small

\- gpt-6-astra

\- ChromaDB

\- Pydantic

\- Git / GitHub

Project Structure

day11/

├── basic\_langchain.py

├── prompt\_chain.py

├── output\_parser.py

├── rag\_chain.py

└── README.md



Key Takeaway

LangChain should not be treated as a replacement for understanding LLM application architecture.

The important engineering skill is understanding:

LLM

&#x20;+

Prompt

&#x20;+

Retrieval

&#x20;+

Tools

&#x20;+

Data

&#x20;+

Workflow

&#x20;=

AI Application



LangChain provides abstractions that help compose these components into maintainable applications.

The goal is to use the framework where it provides real value while understanding the underlying mechanisms well enough to build, debug, evaluate, and optimize the application.

