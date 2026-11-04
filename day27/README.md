\# Day 27 – RAG Evaluation using RAGAS



\## Objective

Build an evaluation pipeline to measure the quality of a Retrieval-Augmented Generation (RAG) system using RAGAS.



\## Concepts Covered

\- RAG evaluation fundamentals

\- Faithfulness

\- Answer Relevancy

\- Context Precision

\- Context Recall

\- LLM-as-a-Judge

\- Evaluation datasets using Hugging Face Dataset

\- OpenAI evaluator integration

\- Combined RAG evaluation



\## Evaluation Metrics



| Metric | Purpose |

|---|---|

| Faithfulness | Measures whether generated answers are supported by retrieved contexts. |

| Answer Relevancy | Measures whether the answer addresses the user's question. |

| Context Precision | Measures whether relevant retrieved contexts are ranked effectively. |

| Context Recall | Measures whether retrieved contexts contain the information needed to answer the question. |



\## Implementation



Created the following Python scripts:



\- `rag\_evaluation.py` – Builds the evaluation dataset.

\- `ragas\_metrics.py` – Configures the evaluator LLM.

\- `faithfulness\_test.py` – Evaluates answer faithfulness.

\- `answer\_relevancy\_test.py` – Evaluates answer relevancy.

\- `context\_precision\_test.py` – Evaluates context precision.

\- `context\_recall\_test.py` – Evaluates context recall.

\- `combined\_evaluation.py` – Runs all four evaluation metrics together.



\## Combined Evaluation Results



| Metric | Score |

|---|---:|

| Faithfulness | 0.8889 |

| Answer Relevancy | 0.9693 |

| Context Precision | 1.0000 |

| Context Recall | 1.0000 |



Note: These results are based on an illustrative dataset containing only three test cases. They are learning results, not production benchmarks.



\## Key Learnings



1\. High faithfulness does not guarantee factual correctness.

2\. Answer relevancy measures whether the response addresses the question.

3\. Context precision focuses on the relevance and ranking of retrieved documents.

4\. Context recall measures retrieval completeness.

5\. Increasing top-k can improve recall but may introduce irrelevant documents.

6\. Hybrid search, reranking, chunking and metadata filtering can improve retrieval quality.

7\. Retrieval metrics and answer-generation metrics should be evaluated separately.



\## Practical Application



Applied RAG evaluation concepts to an enterprise Change Management knowledge assistant to assess whether answers are grounded, relevant and supported by retrieved change-management documentation.



\## Future Improvements



\- Expand the evaluation dataset with diverse enterprise scenarios.

\- Investigate evaluator generation warnings.

\- Modernize the deprecated LangChainLLMWrapper integration.

\- Evaluate response latency and API cost.

\- Compare retrieval strategies using consistent test datasets.

