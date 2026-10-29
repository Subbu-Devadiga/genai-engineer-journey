\# Day 22 — RAG Evaluation Fundamentals



\## Overview



Day 22 focuses on evaluating Retrieval-Augmented Generation (RAG) applications using a small, manually created evaluation dataset.



I built a Python evaluation script to compare generated answers against supporting context and determine whether the answers appear to be supported by the available evidence.



The project builds on previous days of my GenAI Engineer learning journey, particularly RAG, answer validation, conditional routing, and reliable agent design.



\## Learning Objectives



\- Understand the difference between retrieval quality and answer quality.

\- Create a small evaluation dataset for a Change Management AI assistant.

\- Calculate lexical overlap between an answer and its supporting context.

\- Test supported, unsupported, and misleading answers.

\- Evaluate whether the system correctly identifies unanswerable questions.

\- Understand the limitations of heuristic-based grounding checks.

\- Interpret evaluation accuracy without overstating model reliability.



\## Project Architecture



```text

Evaluation Dataset

&#x20;       |

&#x20;       v

Question + Answer + Context

&#x20;       |

&#x20;       v

Extract Meaningful Words

&#x20;       |

&#x20;       v

Calculate Word Overlap

&#x20;       |

&#x20;       v

Compare Against Threshold

&#x20;       |

&#x20;       v

Predicted Support Status

&#x20;       |

&#x20;       v

Compare with Expected Label

&#x20;       |

&#x20;       v

Print Test Results and Accuracy

```



\## Implementation



\### 1. Word-Overlap Score



The `word\_overlap\_score()` function measures how many meaningful words in the answer also appear in the supporting context.



The formula is:



`Overlap Score = Matching Answer Words / Total Meaningful Answer Words`



The implementation uses Python regular expressions to extract words and set intersection to identify matching words. Common stop words are excluded.



\### 2. Support Classification



The evaluation uses a threshold of `0.60`:



\- Score greater than or equal to `0.60`: predicted supported.

\- Score below `0.60`: predicted unsupported.



This is a simple lexical-overlap heuristic for learning purposes. It does not establish factual correctness or semantic entailment.



\### 3. Evaluation Dataset



The script contains four test cases based on Change Management scenarios.



| Test case | Expected classification | Observed score | Result |

|---|---|---:|---|

| Rollback plan | Supported | 1.00 | PASS |

| Emergency change | Supported | 1.00 | PASS |

| Unknown CAB limit | Unsupported | 0.25 | PASS |

| Misleading rollback answer | Unsupported | 0.40 | PASS |



\## Test Results



\*\*Decision accuracy: 4/4 (100%)\*\*



All four test cases were classified according to their expected labels.



The misleading-answer test demonstrates that a response can share some words with the context while still making an unsupported claim. The overlap threshold rejected this example.



However, these results only measure agreement between the heuristic's decisions and the manually assigned labels in this small dataset. They do not demonstrate 100% factual accuracy for a real LLM application.



\## Key Learnings



\### Retrieval Quality vs. Answer Quality



\- \*\*Retrieval quality:\*\* Measures whether relevant documents are retrieved for a question. Common metrics include Recall@K and Precision@K.

\- \*\*Answer quality:\*\* Measures whether the generated response is correct, relevant, complete, and supported by the evidence.



A RAG system needs effective retrieval and reliable answer generation.



\### Unanswerable Questions



Questions whose answers are absent from the knowledge base must also be tested. The system should acknowledge insufficient information rather than inventing enterprise policies or unsupported facts.



\### Evaluation Accuracy



A high score on a small dataset does not prove production readiness. Evaluation should use a larger, representative collection of questions, expected answers, trusted evidence, edge cases, and regression tests.



\## Limitations



1\. \*\*Lexical matching:\*\* The score measures word overlap, not meaning.

2\. \*\*Negation and contradictions:\*\* The heuristic may miss important differences such as "approval is required" versus "approval is not required."

3\. \*\*Paraphrasing:\*\* Correct answers that use different wording may receive low scores.

4\. \*\*Small dataset:\*\* Four test cases are insufficient to establish real-world reliability.

5\. \*\*No live retrieval:\*\* The current script uses manually supplied context rather than retrieving documents from ChromaDB.

6\. \*\*No live LLM evaluation:\*\* The answers are predefined, so the script does not yet evaluate generated model responses.



\## Future Improvements



\- Connect the evaluator to the existing ChromaDB knowledge base.

\- Evaluate answers produced by the actual RAG pipeline.

\- Add Recall@K and Precision@K metrics for retrieval.

\- Test answer relevance, faithfulness, and factual correctness.

\- Include more positive, negative, adversarial, and edge-case examples.

\- Compare heuristic results with human-reviewed labels.

\- Add automated regression tests to track changes over time.



\## Technology Stack



\- Python

\- Regular expressions (`re`)

\- Set operations

\- Lexical-overlap evaluation

\- Manually labelled evaluation dataset





\## Conclusion



Day 22 introduced the fundamentals of RAG evaluation. I created a small evaluation dataset and implemented a word-overlap heuristic to classify answers as supported or unsupported.



This exercise demonstrated how evaluation can expose weaknesses in AI answer validation and why simple metrics should not be mistaken for proof of factual correctness.



The next step is to evaluate answers from the actual Change Management RAG pipeline using retrieved enterprise evidence and more robust evaluation methods.



