\# Day 20 — Reliable AI Agent with LangGraph



\## Overview



On Day 20 of my GenAI Engineer learning journey, I built a reliable AI agent workflow using Python and LangGraph. The project demonstrates answer validation, risk assessment, conditional routing, safe fallback responses, and human-review routing for high-risk requests.



The objective is to prevent unsupported answers from being returned as reliable information and to ensure that high-risk production requests are not automatically approved.



\## Learning Objectives



\- Implement a multi-node workflow using LangGraph.

\- Validate answers against supporting evidence.

\- Handle questions when supporting information is unavailable.

\- Classify requests using basic risk-assessment rules.

\- Route requests dynamically using `add\_conditional\_edges()`.

\- Separate answer validation from authorization decisions.

\- Understand the importance of human review in enterprise AI workflows.



\## Architecture



```text

START

&#x20; |

&#x20; v

Prepare Answer

&#x20; |

&#x20; v

Validate Answer

&#x20; |

&#x20; v

Assess Risk

&#x20; |

&#x20; v

Conditional Router

&#x20; |

&#x20; +---- Approved + Normal Risk

&#x20; |          |

&#x20; |          v

&#x20; |      Return Answer

&#x20; |

&#x20; +---- Rejected + Normal Risk

&#x20; |          |

&#x20; |          v

&#x20; |      Safe Fallback

&#x20; |

&#x20; +---- High Risk

&#x20;            |

&#x20;            v

&#x20;       Human Review

&#x20;            |

&#x20;            v

&#x20;           END

```



\## Workflow Components



\### 1. Prepare Answer



The `prepare\_answer()` node prepares a response and its supporting evidence. In this learning prototype, both are simulated using predefined examples rather than retrieved from a live knowledge base.



\### 2. Validate Answer



The `validate\_answer()` node checks whether the answer is non-empty, supporting evidence exists, and the answer appears literally within that evidence.



This is a basic demonstration of grounding validation, not a complete semantic verification system.



\### 3. Assess Risk



The `assess\_risk()` node uses simple keyword matching to identify potentially high-risk requests, such as production deployment approval.



This demonstrates risk classification but would need stronger rules and trusted change metadata in a production environment.



\### 4. Conditional Routing



The `route\_after\_checks()` function selects the next node:



\- \*\*Approved and normal risk:\*\* Return the answer.

\- \*\*Rejected and normal risk:\*\* Return an insufficient-information response.

\- \*\*High risk:\*\* Route to the human-review node.



The graph uses LangGraph's `add\_conditional\_edges()` method to implement these branches.



\### 5. Safe Fallback



When an answer fails validation, the system avoids inventing enterprise policies and returns an insufficient-information response.



\### 6. Human Review



High-risk requests receive a message indicating that human review is required. The current implementation does not pause execution for an actual reviewer or record an approval decision.



\## Test Cases



| Test case | Validation | Risk | Expected result |

|---|---|---|---|

| What is a rollback plan? | Approved | Normal | Return the supported answer |

| What is the maximum number of CAB members? | Rejected | Normal | Return insufficient information |

| Approve production deployment | Rejected | High | Require human review |



\### Sample Results



\*\*Test 1 — Supported answer\*\*



Question: What is a rollback plan?



Result: Validation approved.



Final answer: A rollback plan explains how to restore the previous working state if a change fails.



\*\*Test 2 — Unsupported answer\*\*



Question: What is the maximum number of CAB members?



Result: Validation rejected.



Final answer: Insufficient information: I cannot provide a reliable answer from the available evidence.



\*\*Test 3 — High-risk request\*\*



Question: Approve production deployment.



Result: Validation rejected; risk classified as high.



Final answer: Human review required before proceeding. No production action has been authorized.



\## Key Learnings



\- The existence of retrieved context does not guarantee that an answer is correct.

\- Answer grounding and risk assessment are separate checks.

\- Conditional edges enable dynamic workflow execution.

\- Unsupported answers should be handled safely.

\- A well-grounded answer does not automatically authorize a production action.

\- Human approval, access control, and policy enforcement are essential for consequential enterprise operations.



\## Limitations and Future Improvements



The current implementation is a learning prototype with several limitations:



1\. \*\*Literal-text validation:\*\* It cannot reliably determine semantic equivalence or whether every claim is supported.

2\. \*\*Keyword-based risk classification:\*\* It may miss high-risk requests that use different wording.

3\. \*\*Simulated retrieval:\*\* Answers and evidence are predefined rather than retrieved from the existing RAG knowledge base.

4\. \*\*Human-review simulation:\*\* The graph returns a review message but does not implement a real approval pause.

5\. \*\*No production authorization:\*\* The application does not execute or approve actual change requests.



Future improvements include integrating the existing RAG pipeline, adding source-aware claim verification, testing edge cases, implementing LangGraph human-in-the-loop interrupts, and enforcing authorization independently of the LLM.



\## Technology Stack



\- Python

\- LangGraph

\- TypedDict

\- Conditional graph routing

\- Answer validation

\- Basic risk classification



\## Project Structure



```text

day20/

├── reliable\_agent.py

└── README.md

```



\## Conclusion



Day 20 strengthened my understanding of reliable GenAI application design. I implemented a conditional LangGraph workflow that distinguishes supported answers, unsupported questions, and high-risk requests.



This project provides a foundation for building an evidence-aware enterprise Change Management AI assistant with stronger validation, policy controls, and human-in-the-loop approval workflows.



