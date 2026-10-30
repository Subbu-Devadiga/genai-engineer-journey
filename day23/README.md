\# Day 23 – RAG Retrieval Evaluation: Precision@K and Recall@K



\## Overview



Day 23 focuses on evaluating the retrieval component of a Retrieval-Augmented Generation (RAG) application.



The objective is to measure how effectively ChromaDB retrieves relevant documents for user queries using two important information retrieval metrics:



\- Precision@K

\- Recall@K



This implementation reuses the Change Management knowledge base created during Day 8 and evaluates retrieval performance across different K values.



\## Learning Objectives



\- Understand Precision@K and Recall@K.

\- Evaluate ChromaDB retrieval performance.

\- Compare retrieved documents against manually labelled expected sources.

\- Experiment with different K values.

\- Understand the trade-off between retrieval relevance and completeness.

\- Identify an appropriate K value for an enterprise RAG application.



\## Concepts Covered



\### 1. Precision@K



Precision measures the proportion of retrieved documents that are relevant.



\*\*Formula:\*\*



Precision@K = Relevant retrieved documents / K



A higher precision indicates that the retriever returns fewer irrelevant documents.



\### 2. Recall@K



Recall measures the proportion of all expected relevant documents that were successfully retrieved.



\*\*Formula:\*\*



Recall@K = Relevant retrieved documents / Total expected relevant documents



A higher recall indicates that the retriever misses fewer relevant documents.



\## Project Architecture



1\. User submits a question.

2\. OpenAI Embeddings convert the question into a vector representation.

3\. ChromaDB retrieves the top-K documents.

4\. Retrieved document source IDs are extracted.

5\. Retrieved sources are compared against manually labelled expected sources.

6\. Precision@K and Recall@K are calculated.

7\. Results are displayed for evaluation.



\## Technology Stack



\- Python

\- OpenAI Embeddings – `text-embedding-3-small`

\- ChromaDB

\- LangChain

\- LangChain Chroma integration

\- python-dotenv



\## Implementation



\*\*File:\*\* `retrieval\_evaluation.py`



The implementation:



\- Connects to the existing Day 8 ChromaDB collection.

\- Defines test questions and expected relevant source IDs.

\- Retrieves documents using similarity search.

\- Calculates Precision@K and Recall@K.

\- Compares retrieval performance at different K values.



\### Test Scenarios



| Test Question | Expected Relevant Sources |

|---|---|

| What is a rollback plan? | rollback |

| What documentation is required for an emergency change? | emergency\_change |

| What should I validate before implementing a production change? | production\_validation, staging\_and\_uat, normal\_change |



\## Experimental Results



The retrieval pipeline was tested with K values of 1, 2, 3, 4 and 5.



\### Production Validation Test Results



| K Value | Precision@K | Recall@K |

|---|---:|---:|

| 1 | 1.00 | 0.33 |

| 2 | 1.00 | 0.67 |

| 3 | 1.00 | 1.00 |

| 4 | 0.75 | 1.00 |

| 5 | 0.60 | 1.00 |



\### Key Observations



\- At K=1, the retriever found one relevant document but missed two other expected documents.

\- At K=2, retrieval completeness improved.

\- At K=3, all three expected relevant documents were retrieved.

\- At K=5, recall remained unchanged while precision decreased because additional documents were retrieved.



For this particular production-validation test, K=3 achieved the best balance, with both precision and recall at 1.00.



Note: These results are based on the manually labelled expected sources and the observed ChromaDB retrieval results.



\## Key Engineering Learnings



1\. High precision does not necessarily mean complete retrieval.

2\. High recall does not necessarily mean all retrieved documents are relevant.

3\. Increasing K can improve recall but may reduce precision.

4\. Ground-truth source labels are essential for objective retrieval evaluation.

5\. A larger K value is not automatically better.

6\. Retrieval evaluation should be combined with answer-quality evaluation.



\## Enterprise Application



In enterprise RAG systems, selecting the appropriate K value is important because:



\- Irrelevant documents increase LLM context consumption.

\- Missing relevant documents can lead to incomplete answers.

\- Larger retrieval sets can increase token usage and latency.

\- Retrieval performance directly influences answer quality.



The optimal K should be selected based on evaluation results, answer quality, latency and cost rather than a fixed assumption.



\## Interview Questions



1\. What is Precision@K?

2\. What is Recall@K?

3\. Can a RAG system have high precision but low recall?

4\. Why do we need manually labelled expected sources?

5\. Why is increasing K not always beneficial?

6\. How would you select the optimal K value for an enterprise RAG application?

7\. What is the difference between retrieval evaluation and answer evaluation?



\## Project Structure



```text

day23/

│

├── retrieval\_evaluation.py

└── README.md

```



\## Conclusion



Day 23 strengthened the understanding of RAG retrieval evaluation through practical experimentation with Precision@K and Recall@K.



The implementation demonstrates how to measure retrieval quality, compare different K values and make evidence-based decisions when optimizing an enterprise RAG pipeline.



