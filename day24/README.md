\# Day 24 – Retrieval Strategy Comparison: Similarity Search vs MMR



\## Overview



Day 24 focuses on comparing two retrieval strategies used in Retrieval-Augmented Generation (RAG) applications:



1\. Similarity Search

2\. Maximum Marginal Relevance (MMR)



The objective is to understand how different retrieval strategies affect document relevance, diversity, answer quality, and the overall performance of an enterprise RAG application.



The experiments use a Change Management knowledge base containing enterprise ITSM documents.



\## Learning Objectives



\- Understand similarity search and MMR.

\- Identify redundant document retrieval.

\- Understand the `fetch\_k` parameter.

\- Understand the `lambda\_mult` parameter.

\- Compare retrieval precision and recall.

\- Evaluate generated answers using retrieved context.

\- Identify suitable retrieval configurations for enterprise RAG applications.



\## 1. Similarity Search



Similarity search retrieves documents based on their semantic similarity to the user's query.



It uses embeddings to identify documents that are closest to the query in vector space.



\*\*Advantages:\*\*

\- Retrieves highly relevant documents.

\- Simple to implement.

\- Useful for semantic questions.



\*\*Limitations:\*\*

\- May retrieve multiple documents containing similar information.

\- Does not explicitly optimize diversity.

\- May miss complementary information required for a complete answer.



\## 2. Maximum Marginal Relevance (MMR)



MMR balances two objectives:



\- Relevance: How closely a document matches the user's question.

\- Diversity: How much new information a document contributes compared with documents already selected.



MMR helps reduce redundant retrieval and can provide a broader range of supporting information.



\### Important parameters



\*\*fetch\_k\*\*



Controls the initial number of candidate documents retrieved before the MMR diversity-selection process.



\*\*lambda\_mult\*\*



Controls the balance between relevance and diversity.



| Lambda value | Retrieval behaviour |

|---|---|

| 0.0 | Prioritizes diversity |

| 0.5 | Balances relevance and diversity |

| 1.0 | Prioritizes relevance |



\## 3. Experimental Configurations



The experiments tested different combinations of `fetch\_k` and `lambda\_mult`.



| fetch\_k | lambda\_mult |

|---:|---:|

| 5 | 0.0 |

| 5 | 0.5 |

| 5 | 1.0 |

| 10 | 0.0 |

| 10 | 0.5 |

| 10 | 1.0 |

| 15 | 0.0 |

| 15 | 0.5 |

| 15 | 1.0 |



Similarity search was also used as the baseline.



\## 4. Evaluation Metrics



\### Precision@K



Measures the proportion of retrieved documents that are relevant.



Precision@K = Relevant retrieved documents / Total retrieved documents



\### Recall@K



Measures the proportion of all expected relevant documents that were retrieved.



Recall@K = Relevant retrieved documents / Total expected relevant documents



\### Answer quality



Retrieval metrics alone are not sufficient. Generated answers must also be evaluated for:



\- Faithfulness to retrieved context.

\- Factual correctness.

\- Completeness.

\- Citation and source accuracy.

\- Appropriate abstention when information is insufficient.



\## 5. Experimental Observations



Three enterprise change-management questions were tested.



\### Test Case 1: Rollback Plan



Expected source: `rollback`



Observations:

\- Similarity search retrieved the required source.

\- MMR retrieved the required source across the tested configurations.

\- Some configurations also retrieved additional documents such as `deployment\_strategy` and `release\_cutover`.

\- The generated answer remained grounded in the rollback document.



\### Test Case 2: Emergency Change Documentation



Expected primary source: `emergency\_change`



Observations:

\- MMR retrieved different combinations of supporting documents depending on the configuration.

\- Some useful additional sources included `cab`, `change\_closure`, and `major\_incident\_management`.

\- Certain configurations generated more complete answers than others.

\- Some configurations returned insufficient information.



\### Test Case 3: Production Change Validation



Expected sources:

\- `normal\_change`

\- `staging\_and\_uat`

\- `production\_validation`



Observations:

\- MMR with `fetch\_k=5` and `lambda\_mult=1.0` retrieved all three expected sources.

\- Precision@3: 1.00

\- Recall@3: 1.00

\- The generated answer incorporated information from all three supporting documents.



This was the best observed result for this test case among the configurations tested.



\## 6. Key Learnings



1\. Similarity search prioritizes semantic relevance.

2\. MMR balances relevance and diversity.

3\. Increasing `fetch\_k` does not automatically improve retrieval quality.

4\. Lowering `lambda\_mult` encourages diversity but may reduce the relevance of selected documents.

5\. Higher `lambda\_mult` prioritizes relevance.

6\. Precision and recall must be evaluated together.

7\. Retrieval quality and answer quality are different evaluation dimensions.

8\. The same LLM and prompt should be used when comparing retrieval strategies to isolate the effect of retrieval.

9\. The expected-source evaluation dataset must be carefully labelled.

10\. Retrieval strategy should be selected based on experimental results rather than assumptions.



\## 7. Enterprise RAG Considerations



For an enterprise RAG application, retrieval strategy should be evaluated using representative questions and a manually verified evaluation dataset.



A practical evaluation process:



1\. Prepare representative enterprise questions.

2\. Identify all documents that legitimately support each answer.

3\. Compare similarity search and MMR.

4\. Experiment with different K, `fetch\_k`, and `lambda\_mult` values.

5\. Calculate precision and recall.

6\. Generate answers using the same LLM and prompt.

7\. Evaluate faithfulness, correctness, completeness, and citations.

8\. Compare latency and token consumption.

9\. Select the strategy that provides the best overall results.



\## 8. Project Structure



```text

day24/

│

├── retrieval\_comparison.py

├── end\_to\_end\_comparison.py

└── README.md

```



\## 9. Technologies Used



\- Python

\- LangChain

\- OpenAI embeddings

\- ChromaDB

\- Vector similarity search

\- Maximum Marginal Relevance (MMR)

\- Retrieval-Augmented Generation (RAG)



\## 10. Conclusion



Day 24 demonstrated that retrieval strategy has a direct impact on the context supplied to an LLM.



Similarity search and MMR both have advantages. Neither should be assumed to be universally better.



The final retrieval strategy should be selected after evaluating retrieval precision, recall, answer faithfulness, factual correctness, completeness, latency, and cost.



The objective is not simply to retrieve more documents, but to retrieve the right evidence to generate reliable and trustworthy enterprise answers.



\---



\*\*Day 24 Status: Completed\*\*



\*\*Next Topic: Day 25 – Hybrid Search (Vector Search + BM25)\*\*

