\# Day 19 — Answer Validation and Conditional Routing with LangGraph



\## Overview



On Day 19, I enhanced my enterprise Change Management AI assistant by introducing answer validation and conditional routing using LangGraph.



The objective was to ensure that the agent does not provide unsupported answers when the retrieved context is missing or the generated response is unusable. Instead, the graph routes the response through different paths depending on the validation result.



\## Learning Objectives



\- Understand why checking for context alone does not guarantee answer accuracy.

\- Implement basic answer-validation checks.

\- Return an insufficient-information response when a reliable answer cannot be produced.

\- Use LangGraph conditional edges to route execution dynamically.

\- Separate answer validation from final-answer generation.

\- Understand where human review may be required in enterprise workflows.



\## Key Concepts



\### 1. Answer Validation



Answer validation checks whether the generated answer is suitable to return to the user.



For example:



\*\*Question:\*\* What is a rollback plan?



\*\*Result:\*\* Validation approved basic checks.



\*\*Final answer:\*\* A rollback plan explains how to restore the previous working state if a change fails.



However, a question such as "What is the maximum number of CAB members?" must not receive an invented answer if the knowledge base contains no supporting information.



\### 2. Why Context Existence Is Not Enough



The presence of retrieved context does not prove that an answer is correct.



\- The retrieved document may be irrelevant.

\- The document may contain outdated or incorrect information.

\- The answer may make claims that are not supported by the retrieved text.

\- The information may be insufficient to answer the exact question.



A production-grade system should assess relevance, source reliability, and answer grounding—not merely whether a document was retrieved.



\### 3. Conditional Routing in LangGraph



LangGraph provides two useful routing mechanisms:



\- `add\_edge()`: Defines a fixed transition between graph nodes.

\- `add\_conditional\_edges()`: Selects the next node based on a routing function and the current state.



In this project, the router examines `state\["status"]` to decide which path to follow.



Conceptual workflow:



```text

START

&#x20; |

&#x20; v

Generate / Prepare Answer

&#x20; |

&#x20; v

Validate Answer

&#x20; |

&#x20; v

Conditional Router

&#x20; |

&#x20; +---- Approved ----> Return Answer

&#x20; |

&#x20; +---- Rejected ----> Insufficient-Information Response

&#x20; |

&#x20; v

&#x20;END

```



The router determines the execution path. It does not independently generate the final answer.



\### 4. Insufficient-Information Handling



When the system cannot establish a reliable answer, it should respond transparently rather than inventing enterprise procedures or policies.



Example:



\*\*Question:\*\* What is the maximum number of CAB members?



\*\*Final answer:\*\* Insufficient information: I cannot provide a reliable answer because supporting context or a usable answer is missing.



This approach reduces the risk of misleading users about change-management requirements.



\## Test Cases



| Test case | Question | Expected behavior |

|---|---|---|

| 1 | What is a rollback plan? | Approve when the answer passes the configured checks |

| 2 | What is the maximum number of CAB members? | Reject if supporting information is unavailable |

| 3 | What is a rollback plan? | Reject if the answer is unusable or required supporting context is missing |



\*\*Important:\*\* Test case 3 demonstrates that a relevant question can still receive a rejected result if the validation stage cannot establish a usable answer. This is a useful debugging case: investigate retrieval, answer generation, and validation logic before concluding that the knowledge base lacks the answer.



\## Enterprise Application



In an enterprise Change Management assistant, the same pattern can help with questions about:



\- Change implementation and rollback plans

\- CAB and ECAB procedures

\- Risk and impact assessments

\- UAT and production validation

\- Emergency-change documentation

\- Change approvals and closure requirements



For high-risk production decisions, passing basic answer-validation checks must not automatically authorize the change. Stronger policy checks, authorization controls, and human approval may still be necessary.



\## Security and Reliability Considerations



\- Retrieve information from approved enterprise sources.

\- Validate the relevance and reliability of supporting documents.

\- Distinguish factual answers from recommendations.

\- Avoid inventing policy when evidence is missing.

\- Keep approval decisions separate from informational responses.

\- Route high-risk or ambiguous cases for human review.

\- Log validation outcomes and relevant source references for auditability.



\## Interview Questions and Answers



\### 1. What is the difference between `add\_edge()` and `add\_conditional\_edges()`?



`add\_edge()` defines a fixed transition between nodes. `add\_conditional\_edges()` uses a routing function to select the next node based on the current state or other runtime conditions.



\### 2. Why does the router inspect `state\["status"]`?



The router uses the validation status to choose the appropriate execution path. For example, an approved result can proceed to the normal response node, while a rejected result can proceed to a safe fallback response.



\### 3. Why should an agent return "insufficient information"?



It prevents the system from inventing unsupported enterprise policies, which could cause operational errors, compliance problems, or loss of user trust.



\### 4. Why is checking that context exists insufficient?



Retrieved context can be irrelevant, outdated, inaccurate, or insufficient. The system must evaluate whether the answer is actually supported by the evidence.



\### 5. Should a grounded answer automatically approve a high-risk production change?



No. Grounding supports the reliability of an informational answer, but production approval also requires risk assessment, authorization, change-policy compliance, and potentially human review.



\### 6. Where could human review be added?



A human-review node can be placed after validation and risk classification but before a consequential approval or execution action. The graph should pause for an authorized reviewer when required.



\## Day 19 Summary



Today I learned how to validate generated answers, handle unsupported questions safely, and use LangGraph conditional routing to direct execution based on validation status.



This improves the reliability of my enterprise AI assistant and establishes a foundation for more advanced workflows involving policy checks, risk-based routing, human-in-the-loop review, and evaluation.



\## Technology Stack



\- Python

\- LangGraph

\- LangChain / LLM integration

\- Enterprise Change Management knowledge base

\- Answer validation

\- Conditional workflow routing



\## Next Steps



\- Improve validation beyond basic checks.

\- Verify that generated claims are supported by retrieved sources.

\- Add source references to final answers.

\- Add a human-review branch for high-risk cases.

\- Create automated tests for approved, rejected, and uncertain answers.



