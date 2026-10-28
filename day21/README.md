\# Day 21 — GenAI Agent Evaluation and Testing



\## Overview



Day 21 focuses on evaluating the reliability of GenAI applications using Python testing techniques. I extended my enterprise Change Management AI agent project to test answer validation, missing evidence, unsupported answers, and conditional routing.



The main objective is to demonstrate how automated tests can identify weaknesses in an AI workflow and help prevent unsupported responses from being treated as reliable information.



\## Learning Objectives



\- Understand the difference between code testing and LLM evaluation.

\- Create test cases for supported and unsupported answers.

\- Validate the presence of answers and supporting context.

\- Use a word-overlap heuristic to check basic evidence alignment.

\- Test conditional routing for normal-risk and high-risk requests.

\- Understand the limitations of simple grounding validation.

\- Apply regression testing to improve agent reliability.



\## Project Architecture



```text

Test Cases

&#x20;   |

&#x20;   v

Answer Validation

&#x20;   |

&#x20;   +---- Valid answer and evidence

&#x20;   |             |

&#x20;   |             v

&#x20;   |      Approved for Response

&#x20;   |

&#x20;   +---- Missing or unsupported evidence

&#x20;                 |

&#x20;                 v

&#x20;         Insufficient Information



Risk Assessment

&#x20;   |

&#x20;   +---- Normal Risk

&#x20;   |        |

&#x20;   |        v

&#x20;   |   Normal Workflow

&#x20;   |

&#x20;   +---- High Risk

&#x20;            |

&#x20;            v

&#x20;       Human Review

```



The validation and routing examples are implemented as separate Python functions. This makes the logic easier to test and maintain.



\## Implementation



\### 1. Basic Answer Validation



The `validate\_answer()` function checks whether:



\- The answer is not empty.

\- Supporting context is available.

\- The answer contains a sufficient proportion of meaningful words found in the context.



The implementation uses Python regular expressions to extract words and a set-intersection operation to calculate word overlap.



\### 2. Word-Overlap Heuristic



The validator calculates:



`overlap ratio = matching answer words / meaningful answer words`



The current implementation accepts an answer when the overlap ratio is at least `0.6` (60%).



This is a lightweight heuristic for learning and testing. It does not establish that the answer is factually correct or semantically supported.



\### 3. Conditional Routing



The `route\_request()` function selects a workflow outcome based on risk and validation status.



| Condition | Expected route |

|---|---|

| Validation passes and risk is normal | `approved\_for\_response` |

| Validation fails | `insufficient\_information` |

| Validation passes and risk is high | `human\_review` |



Validation failure takes precedence over risk classification in this simplified routing function.



\## Test Cases and Results



The following four test cases were executed successfully.



| Test case | Expected behavior | Result |

|---|---|---|

| Supported answer | Accept the answer | PASS |

| Missing context | Reject the answer | PASS |

| Empty answer | Reject the answer | PASS |

| Unsupported answer with context present | Reject based on the overlap threshold | PASS |



\*\*Test summary: 4/4 tests passed.\*\*



The unsupported-answer test was particularly important because it exposed a weakness in the original implementation, which checked only whether the answer and context were non-empty.



\## Key Learnings



\- Code execution alone does not prove an AI application is reliable.

\- Automated tests can expose weaknesses in answer-validation logic.

\- The existence of context does not guarantee factual correctness.

\- Word overlap can help identify some unsupported claims but cannot verify meaning.

\- Regression tests help prevent previously fixed issues from returning.

\- High-risk enterprise actions require separate authorization and review controls.



\## Limitations



This project is a learning prototype and has the following limitations:



1\. \*\*Lexical matching:\*\* The validator relies on word overlap rather than semantic entailment or claim-level verification.

2\. \*\*False positives:\*\* An incorrect answer may share many words with the context and still pass.

3\. \*\*False negatives:\*\* A correct paraphrase may use different words and fail the threshold.

4\. \*\*No live LLM evaluation:\*\* The current tests use predefined answers rather than systematically evaluating generated model responses.

5\. \*\*Simplified risk assessment:\*\* Risk categories are provided to the routing function rather than derived from a complete enterprise risk model.

6\. \*\*No actual approval mechanism:\*\* The human-review route is a label or workflow outcome, not a fully implemented approval process.



\## Future Improvements



\- Integrate the existing RAG pipeline and real Change Management knowledge base.

\- Evaluate answers against trusted source documents and citations.

\- Add claim-level grounding checks and human-reviewed evaluation examples.

\- Measure answer relevance, faithfulness, and correct abstention.

\- Expand automated tests with edge cases and regression scenarios.

\- Implement LangGraph human-in-the-loop approval for high-risk actions.

\- Record evaluation results to compare different prompts, models, and retrieval configurations.



\## Technology Stack



\- Python

\- LangGraph concepts and conditional routing

\- Regular expressions

\- Set operations

\- Automated test cases

\- Evidence-alignment heuristics



\## Project Structure



```text

day21/

├── evaluation\_basics.py

└── README.md

```



\## Conclusion



Day 21 demonstrates how automated testing can expose reliability problems in GenAI applications. By testing supported answers, missing context, empty responses, and unsupported answers with available context, I improved my understanding of grounding validation and safe fallback behavior.



This work provides a foundation for more advanced LLM evaluation and testing within an enterprise Change Management AI assistant.



