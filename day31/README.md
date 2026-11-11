\# Day 31 – Context Relevance, Sufficiency Evaluation and Safe RAG Responses



\## Objective

Improve the enterprise RAG application by evaluating whether retrieved documents are relevant to the user's question and whether they contain sufficient information to generate a reliable answer.



\## Topics Covered

\- Context relevance evaluation

\- Context sufficiency evaluation

\- Identifying incomplete or missing information

\- Safe response generation

\- Insufficient-information handling

\- Avoiding hallucinations in enterprise RAG applications

\- Source-aware retrieval and answer generation



\## Implementation

Enhanced the LangGraph-based RAG workflow to evaluate retrieved context before generating the final answer.



The workflow:

1\. Routes the user's question to the appropriate retrieval strategy.

2\. Retrieves relevant documents from ChromaDB.

3\. Evaluates the relevance and sufficiency of retrieved context.

4\. Generates an answer only when sufficient information is available.

5\. Returns a safe insufficient-information response when the knowledge base does not contain enough information.



\## Test Scenarios



| Question | Evaluation | Expected Behaviour |

|---|---|---|

| What is the rollback procedure? | Insufficient | Return safe response because execution steps are missing |

| Find emergency changes related to SAP in production. | Insufficient | Return safe response because SAP-specific records are missing |

| Compare recovery procedures for failed production deployments. | Insufficient | Return safe response because detailed procedures and comparison criteria are missing |



\## Key Learnings

\- Relevant documents may still lack sufficient information to answer a question completely.

\- Retrieval quality and answer quality must be evaluated separately.

\- Enterprise RAG applications should avoid generating unsupported operational instructions.

\- Source attribution improves answer traceability.

\- Safe fallback mechanisms improve reliability and user trust.



\## Day 31 Outcome

Successfully implemented and tested context sufficiency evaluation with safe insufficient-information responses in the enterprise Change Management RAG application.



\*\*Project:\*\* Enterprise Change Management AI Assistant  

\*\*Framework:\*\* LangGraph, LangChain, ChromaDB, OpenAI  



