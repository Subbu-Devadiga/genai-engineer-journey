import os
from dotenv import load_dotenv
from pydantic import BaseModel,Field
from typing import TypedDict,List,Literal

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph,START,END

load_dotenv("../.env")
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("API key not found..")

llm=ChatOpenAI(
    model="gpt-6-astra",
    temperature=1
)

class RAGState(TypedDict):
    question: str
    context: str
    answer: str 
    claims: list[str] 
    verification_results: list[dict]
    supported_claims: list[str]
    unsupported_claims: list[str]
    retry_count: int
    validation_status : str
    validation_reason: str
    final_answer: str
    context_status: str 

class ClaimExtraction(BaseModel):
    claims: list[str] = Field(
        description="List of individual factual claims extracted from the answer"
    )


class ClaimVerification(BaseModel):
    claim: str = Field(
        description="The factual claim being verified"
    )

    status: Literal["SUPPORTED", "UNSUPPORTED"] = Field(
        description="Whether the retrieved context supports the claim"
    )

    reason: str = Field(
        description="Explain why the claim is supported or unsupported"
    )


class ClaimVerificationResults(BaseModel):
    results: list[ClaimVerification] = Field(
        description="Verification result for every factual claim"
    )


print("Enterprise RAG shared state created successfully.....")

class ContextCheckResult(BaseModel):
    context_status : str = Field(
        description="Must be SUFFICIENT or INSUFFICIENT"
    )

    reason : str =Field(
        description="Explain why the retrieved context is sufficient or insufficient"
    )

Context_prompt=ChatPromptTemplate.from_template(
    """
    You are an enterprise RAG context evaluation expert.

Evaluate whether the retrieved context contains enough
relevant information to answer the user's question.

Rules:
1. Use only the retrieved context.
2. Check whether the context addresses the actual question.
3. Do not assume missing information.
4. If important information is missing, mark INSUFFICIENT.
5. Return SUFFICIENT only when the context contains
   enough information to answer the question.

Question:
{question}

Retrieved Context:
{context}

    """
)

context_chain=Context_prompt | llm.with_structured_output(ContextCheckResult)


def context_succiciency_node(state: RAGState):
    print("\nChecking context Sufficiency........")
    result=context_chain.invoke({
        "question" : state["question"],
        "context" : state["context"]
    })

    print("Context status : ",result.context_status)
    print("Reason : ",result.reason)

    return {
        "context_status" : result.context_status
    }


Knowledge_Base=[
    {
        "source": "production_validation",
        "content": (
            "Production changes require application health checks, "
            "functional testing, monitoring and log verification."
        )
    },
    {
        "source": "rollback_procedure",
        "content": (
            "Rollback procedures must be documented before implementation. "
            "If a change causes critical business disruption, the team "
            "should execute the approved rollback plan."
        )
    },
    {
        "source": "change_closure",
        "content": (
            "After successful implementation, record implementation "
            "results, validation results, incidents and issues "
            "before closing the change."
        )
    }
]

def retrieval_node(state : RAGState):
    print("\nRetrieving enterprise documents............")

    retrieved_documents=Knowledge_Base
    context="\n\n".join(
        f"Source :{doc["source"]} \n {doc["content"]}"
        for doc in retrieved_documents
    )

    print("Retrieved documents:",len(retrieved_documents))

    return {
        "context" : context
    }

def route_context(state: RAGState):
    if state["context_status"]=="SUFFICIENT":
        print("Context is sufficient proceeding to answer generation......")

        return "generate_answer"

    else : 
        print("Context is insufficient,executing safe fallback...")

        return "fallback"




answer_prompt=ChatPromptTemplate.from_template(
    """
    You are an enterprise change management assistant.

Answer the user's question using ONLY the retrieved context.

Rules:
1. Do not introduce information that is not present in the context.
2. Do not make unsupported assumptions.
3. Keep the answer clear and concise.
4. Include the relevant source names where possible.

Question:
{question}

Retrieved Context:
{context}
    """
)

answer_chain=answer_prompt | llm

def generate_answer_node(state : RAGState):
    print("\nGenerating grounded answer......")

    result=answer_chain.invoke({
        "question" : state["question"],
        "context" : state["context"]
    })

    answer=result.content
    print("Generated answer : ",answer)
    return {
        "answer" : answer,
        "final_answer" : answer
    }


def fallback_node(state: RAGState):
    print("\nExecuting safe fallback...")

    fallback_answer=(
        "I cannot provide a reliable answer because "
        "the available knowledge base does not contain "
        "sufficient information to answer your question. "
        "Please consult the relevant approved documentation."
    )

    return {
        "final_answer" : fallback_answer,
        "context_status" : "INSUFFICIENT_CONTEXT"
    }


claim_extraction_prompt = ChatPromptTemplate.from_template("""
You are an expert factual claim extraction system.

Extract all individual factual claims from the generated answer.

Rules:
1. Identify every factual statement.
2. Split multiple factual statements into separate claims.
3. Do not add new information.
4. Do not correct or rewrite the claims.
5. Ignore headings and formatting.
6. Return only the extracted claims.

Generated Answer:
{answer}
""")

claim_extraction_chain = (
    claim_extraction_prompt
    | llm.with_structured_output(ClaimExtraction)
)

claim_verification_prompt = ChatPromptTemplate.from_template("""
You are an enterprise RAG claim verification expert.

Your task is to verify each factual claim using ONLY
the provided retrieved context.

Rules:
1. Verify every claim independently.
2. Mark SUPPORTED only when the context provides
   sufficient evidence for the claim.
3. Mark UNSUPPORTED when the context does not mention
   or justify the claim.
4. Do not use external knowledge.
5. Do not assume missing information.
6. Provide a clear reason for every decision.
7. Return one verification result for every input claim.

Retrieved Context:
{context}

Claims to Verify:
{claims}
""")

claim_verification_chain = (
    claim_verification_prompt
    | llm.with_structured_output(ClaimVerificationResults)
)

def claim_extraction_node(state: RAGState):
    print("\nExtracting factual claims.........")

    result = claim_extraction_chain.invoke({
        "answer": state["answer"]
    })

    return {
        "claims": result.claims
    }

def verify_claims_node(state: RAGState):

    print("\nVerifying individual claims.....")

    result = claim_verification_chain.invoke({
        "context": state["context"],
        "claims": "\n".join(state["claims"])
    })

    verification_results = []

    for item in result.results:

        verification_results.append({
            "claim": item.claim,
            "status": item.status,
            "reason": item.reason
        })

    supported_claims = [
        item["claim"]
        for item in verification_results
        if item["status"] == "SUPPORTED"
    ]

    unsupported_claims = [
        item["claim"]
        for item in verification_results
        if item["status"] == "UNSUPPORTED"
    ]

    return {
        "verification_results": verification_results,
        "supported_claims": supported_claims,
        "unsupported_claims": unsupported_claims
    }

def evaluate_claims_node(state: RAGState):

    supported_count = len(state["supported_claims"])
    unsupported_count = len(state["unsupported_claims"])

    print("\nEvaluating claim validation results...")
    print("Supported claims:", supported_count)
    print("Unsupported claims:", unsupported_count)

    if unsupported_count == 0:
        return {
            "validation_status": "VALID",
            "validation_reason": "All factual claims are supported by retrieved context."
        }

    return {
        "validation_status": "INVALID",
        "validation_reason": (
            f"{unsupported_count} factual claim(s) are not supported "
            "by the retrieved context."
        )
    }
def return_answer_node(state: RAGState):
    print("\nAll claims are supported. Returning answer...")

    return {
        "final_answer": state["answer"]
    }
MAX_RETRIES = 3

def route_claim_validation(state: RAGState):

    if state["validation_status"] == "VALID":
        return "return_answer"

    if state["retry_count"] < MAX_RETRIES:
        return "regenerate_answer"

    return "fallback"

regeneration_prompt = ChatPromptTemplate.from_template("""
You are an enterprise RAG answer regeneration expert.

Generate a revised answer using ONLY the supplied context
and supported claims.

Rules:
1. Retain all relevant supported claims.
2. Do not include unsupported claims.
3. Do not introduce new factual information.
4. Answer the original question clearly.
5. If information is unavailable, do not invent it.

Question:
{question}

Retrieved Context:
{context}

Supported Claims:
{supported_claims}
""")

regeneration_chain = regeneration_prompt | llm

def regenerate_answer_node(state: RAGState):

    print("\nRegenerating answer using supported claims...")

    revised_answer = regeneration_chain.invoke({
        "question": state["question"],
        "supported_claims": "\n".join(state["supported_claims"]),
        "context": state["context"]
    })

    return {
        "answer": revised_answer.content,
        "retry_count": state["retry_count"] + 1
    }


workflow=StateGraph(RAGState)

workflow.add_node("retrieval",retrieval_node)
workflow.add_node("check_context",context_succiciency_node)
workflow.add_node("generate_answer",generate_answer_node)
workflow.add_node("fallback",fallback_node)
workflow.add_node("extract_claims", claim_extraction_node)
workflow.add_node("verify_claims", verify_claims_node)
workflow.add_node("evaluate_claims", evaluate_claims_node)
workflow.add_node("return_answer", return_answer_node)
workflow.add_node("regenerate_answer", regenerate_answer_node)
workflow.add_edge(START,"retrieval")
workflow.add_edge("retrieval","check_context")

workflow.add_conditional_edges(
    "check_context",
    route_context,
    {
        "generate_answer" : "generate_answer",
        "fallback" : "fallback"
    }
)

workflow.add_edge("generate_answer", "extract_claims")
workflow.add_edge("extract_claims", "verify_claims")
workflow.add_edge("verify_claims", "evaluate_claims")
workflow.add_conditional_edges(
    "evaluate_claims",
    route_claim_validation,
    {
        "return_answer": "return_answer",
        "regenerate_answer": "regenerate_answer",
        "fallback" : "fallback"
    }
)
workflow.add_edge("return_answer",END)
workflow.add_edge("regenerate_answer","extract_claims")
workflow.add_edge("fallback",END)

app=workflow.compile()

print("\nENterprise RAG Langgraph workflow compiled successfully")


if __name__ == "__main__":

    test_cases = [
        {
            "name": "Sufficient context - supported answer",
            "question": "What activities should be performed after a production change?",
            "expected_context": "SUFFICIENT"
        },
        {
            "name": "Insufficient context - safe fallback",
            "question": "How should database backup restoration be performed after deployment?",
            "expected_context": "INSUFFICIENT_CONTEXT"
        }
    ]

    for test in test_cases:

        print("\n================================")
        print(test["name"])
        print("================================")

        initial_state = {
            "question": test["question"],
            "context": "",
            "answer": "",
            "claims": [],
            "verification_results": [],
            "supported_claims": [],
            "unsupported_claims": [],
            "retry_count": 0,
            "validation_status": "",
            "validation_reason": "",
            "final_answer": "",
            "context_status": ""
        }

        result = app.invoke(initial_state)

        print("\n========== FINAL EXECUTION RESULT ==========")

        print("Context status:", result["context_status"])
        print("Validation status:", result["validation_status"])
        print("Retry count:", result["retry_count"])
        print("Supported claims:", len(result["supported_claims"]))
        print("Unsupported claims:", len(result["unsupported_claims"]))
        print("Final answer:", result["final_answer"])

        print("\nExpected context:", test["expected_context"])

        if result["context_status"] == test["expected_context"]:
            print("TEST RESULT: PASSED")
        else:
            print("TEST RESULT: FAILED")
