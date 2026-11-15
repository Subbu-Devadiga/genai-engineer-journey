\# Day 34 – Answer Faithfulness Validation with LangGraph



\## Objective



Implement an answer validation workflow using LangChain and LangGraph to identify unsupported factual claims in LLM-generated answers and prevent unreliable responses from reaching users.



\## 1. Concepts Covered



\### Grounded Answer Generation

Grounded answer generation ensures that an LLM generates responses strictly based on the retrieved documents rather than relying on external or pretrained knowledge.



\### Answer Faithfulness Validation

Answer faithfulness validation evaluates whether the factual claims in a generated answer are supported by the retrieved context.



A citation being present does not automatically mean an answer is correct. The cited source must actually support the associated claim.



\### Context Sufficiency vs Answer Faithfulness



| Context Sufficiency | Answer Faithfulness |

|---|---|

| Evaluates retrieved documents | Evaluates generated answers |

| Checks whether enough information exists | Checks whether claims are supported |

| Happens before answer generation | Happens after answer generation |

| Prevents generation with insufficient context | Detects unsupported claims |



\## 2. Structured Output with Pydantic



Implemented a Pydantic model to enforce a structured validation response.



The validation result contains:



\- `validation\_status`: VALID or INVALID

\- `validation\_reason`: Explanation of the validation decision



Used LangChain structured output to obtain the validation result from the LLM.



\## 3. LangGraph Workflow



Implemented three workflow nodes:



1\. \*\*Validate Answer Node\*\*

&#x20;  - Evaluates the generated answer against retrieved context.

&#x20;  - Checks whether factual claims are supported.

&#x20;  - Checks whether cited sources support their associated claims.



2\. \*\*Return Answer Node\*\*

&#x20;  - Returns the original generated answer when validation succeeds.



3\. \*\*Fallback Node\*\*

&#x20;  - Returns a safe response when validation fails.

&#x20;  - Prevents unsupported answers from reaching the user.



\### Conditional Routing



\- VALID → Return Answer Node

\- INVALID → Fallback Node



Workflow:



```text

START

&#x20; |

&#x20; v

Validate Answer Node

&#x20; |

&#x20; v

Conditional Routing

&#x20; |

&#x20; |---- VALID ----> Return Answer Node ----> END

&#x20; |

&#x20; |---- INVALID --> Fallback Node ---------> END

```



\## 4. Practical Implementation



Created:



`answer\_validation.py`



Technologies used:



\- Python

\- LangChain

\- LangGraph

\- Pydantic

\- OpenAI API



The workflow uses `ChatOpenAI` with the `gpt-6-astra` model and Pydantic structured output for answer validation.



\## 5. Test Cases and Results



\### Test Case 1 – Valid Answer



\*\*Question:\*\* What activities should be performed after a production change?



\*\*Retrieved Context:\*\*

\- Application health checks

\- Functional testing

\- Monitoring

\- Log verification



\*\*Generated Answer:\*\*



Application health checks, functional testing, monitoring and log verification.



\*\*Expected Result:\*\* VALID



\*\*Actual Result:\*\* VALID



\*\*Workflow:\*\* Validation passed → Return Answer Node.



\### Test Case 2 – Invalid Answer



\*\*Question:\*\* What activities should be performed after a production change?



\*\*Retrieved Context:\*\*

\- Application health checks

\- Functional testing

\- Monitoring

\- Log verification



\*\*Generated Answer:\*\*



Application health checks, functional testing, monitoring, log verification and database backup restoration.



\*\*Expected Result:\*\* INVALID



\*\*Actual Result:\*\* INVALID



\*\*Reason:\*\* The retrieved context does not support database backup restoration as a required activity.



\*\*Workflow:\*\* Validation failed → Fallback Node.



\*\*Fallback Response:\*\*



"I cannot provide a reliable answer because the generated response contains claims that are not sufficiently supported by the knowledge base. Please consult the relevant approved documentation."



\## 6. Important Debugging Lesson



Initially, the workflow was routing every answer to the fallback node.



The issue was a spelling mistake in the state update:



Incorrect:



```python

"validatio\_status": result.validation\_status

```



Correct:



```python

"validation\_status": result.validation\_status

```



The state key must match the key defined in the LangGraph state schema and accessed by the conditional routing function.



\## 7. Key Learnings



\- Grounded answer generation and answer faithfulness validation serve different purposes.

\- Citations alone do not guarantee factual correctness.

\- Pydantic structured output helps enforce predictable validation results.

\- LangGraph conditional edges allow execution to depend on validation results.

\- Unsupported answers should be rejected and routed to a safe fallback.

\- State dictionary keys must match the defined state schema.

\- Context sufficiency and answer faithfulness together improve enterprise RAG reliability.



\## 8. Interview Takeaway



In an enterprise RAG application, context sufficiency evaluates whether retrieved documents contain enough information to answer a query. Answer faithfulness evaluates whether the generated answer is actually supported by those documents.



Both checks are essential. Context sufficiency helps prevent answers from being generated when information is missing, while faithfulness validation identifies unsupported claims in generated responses. LangGraph conditional routing can then return valid answers or execute a safe fallback for invalid answers.



\## 9. Execution



Run the implementation:



```bash

python answer\_validation.py

```



Expected results:



\- Valid answer test → VALID

\- Invalid answer test → INVALID

\- Invalid answer → Safe fallback response



\---



\*\*Day 34 Status: Completed\*\*



Implemented and tested an answer faithfulness validation workflow using Pydantic structured output and LangGraph conditional routing.

