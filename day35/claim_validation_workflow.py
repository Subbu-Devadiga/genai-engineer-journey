from typing import TypedDict,List
from langgraph.graph import StateGraph,START,END
import os
from dotenv import load_dotenv
from pydantic import BaseModel,Field

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv("../.env")

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("API Key not found")

llm=ChatOpenAI(
    model="gpt-6-astra",
    temperature=1
)

class ClaimValidationState(TypedDict):
    question : str
    context : str
    answer :str
    claims: List[str]
    verification_results : List[dict]
    revised_answer : str
    retry_count : int
    max_retries : int
    final_answer : str
    validation_status : str

class ClaimExtraction(BaseModel):
    claims : List[str]=Field(
        description="Individual factual claims extracted from answer"
    )

class claimVerification(BaseModel):
    claim : str =Field(
        description="The original Factual claim"
    )

    status : str =Field(
        description="Must be SUPPORTED or UNSUPPORTED "
    )

    reason : str = Field(
        description="Explain whether context supports this claim"
    )

class ClaimVerificationResults(BaseModel):
    results : List[claimVerification] = Field(
        description="Verification result for every claim"
    )

claim_extraction_prompt=ChatPromptTemplate.from_template(
    """
    You are a factual claim extraction expert.

Extract every individual factual claim from the answer.
Do not add new information.
Ignore headings and conversational filler.

Answer:
{answer}
    """
)

claim_extraction_chain=claim_extraction_prompt | llm.with_structured_output(ClaimExtraction)

def claim_extraction_node(state : ClaimValidationState):
    print("\nExtracting factual claims.........")

    result=claim_extraction_chain.invoke({
        "answer": state["answer"]
    })

    print("\nExtracted claims:")
    for index,claim in enumerate(result.claims,start=1):
        print(f"{index}. {claim}")

    return {
        "claims": result.claims
    }


verification_prompt=ChatPromptTemplate.from_template(
    """
    You are an enterprise RAG claim verification expert.

Verify each claim using ONLY the provided context.

Rules:
1. Mark SUPPORTED only if the context directly supports the claim.
2. Mark UNSUPPORTED if the context does not support the claim.
3. Do not use external knowledge.
4. Evaluate every claim independently.
5. Do not assume that a related statement proves a claim.

Context:
{context}

Claims:
{claims}
    """
)

verification_chain=verification_prompt | llm.with_structured_output(ClaimVerificationResults)


def verify_claims_node(state: ClaimValidationState):
    print("\nVerfying individual claims.....")

    result=verification_chain.invoke({
        "context" : state["context"],
        "claims" : "\n".join(state["claims"])
    })

    verification_results=[]
    for item in result.results:
        print("Claim : ",item.claim)
        print("Status : ",item.status)
        print("Reason : ",item.reason)

        verification_results.append({
            "claim" : item.claim,
            "status" : item.status,
            "reason" : item.reason
        })

    return {
        "verification_results" : verification_results
    }


def decide_claims_node(state : ClaimValidationState):
    print("\nEvaluating claim verification results......")

    if not state["verification_results"]:
        return {
            "validation_status" : "INVALID",
            "revised_answer" : ""
        }

    supported_claims=[]
    unsupported_claims=[]

    for item in state["verification_results"]:
        if item["status"].upper() == "SUPPORTED":
            supported_claims.append(item["claim"])

        else:
            unsupported_claims.append(item["claim"])

    print("\nSupported claims : ",len(supported_claims))
    print("Unsupported claims : ",len(unsupported_claims))

    return {
        "validation_status" : (
            "VALID" if not unsupported_claims else "INVALID"
        ),
        "revised_answer" : "\n".join(supported_claims)
    }


revision_prompt=ChatPromptTemplate.from_template(
    """
    You are an enterprise RAG answer refinement assistant.

Rewrite the answer using ONLY the supported claims below.

Rules:
1. Do not include unsupported claims.
2. Do not introduce new facts.
3. Preserve the meaning of supported claims.
4. Keep the answer clear and concise.
5. Use only the provided context.

Question:
{question}

Context:
{context}

Supported claims:
{supported_claims}

Return only the revised answer.
    """
)

revision_chain=revision_prompt | llm 

def revise_answer_node(state : ClaimValidationState):
    print("\nRegenerating answer using supported claims.....")

    supported_claims=[
        item["claim"]
        for item in state["verification_results"]
        if item["status"].upper()=="SUPPORTED"
    ]

    if not supported_claims:
        return {
            "answer" : "",
            "revised_answer" : "",
            "retry_count" : state["retry_count"]+1
        }

    result= revision_chain.invoke({
        "question" : state["question"],
        "context" : state["context"],
        "supported_claims" : "\n".join(supported_claims)
    })

    revised_answer=result.content

    print("\nRevised answer : ")
    print(revised_answer)

    return {
        "answer" : revised_answer,
        "revised_answer" : revised_answer,
        "retry_count" : state["retry_count"]+1
    }


# def revalidate_answer_node(state : ClaimValidationState):
#     print("\nRevalidating revised answer.....")

#     if not state["revised_answer"].strip():
#         return {
#             "validation_status" : "INVALID",
#             "final_answer" : ""
#         }

#     #extract claims from revised answer
#     extracted=claim_extraction_chain.invoke({
#         "answer" : state["revised_answer"]
#     })

#     verified=verification_chain.invoke({
#         "context" : state["context"],
#         "claims" : "\n".join(extracted.claims)
#     })

#     all_supported=(
#         bool(verified.results)
#         and all(
#             item.status.upper()=="SUPPORTED"
#             for item in verified.results
#         )
#     )

#     if all_supported:
#         print("Revised answer passed validation.. ")

#         return {
#             "validation_status" : "VALID",
#             "final_answer" : state["revised_answer"]
#         }

#     print("Revised answer failed validation...")

#     return {
#         "validation_status" : "INVALID",
#         "final_answer" : ""
#             }


def fallback_node(state: ClaimValidationState):
    print("\nExecuting safe fallback....")
    return {
        "final_answer" : (
            "I cannot provide a reliable answer based on "
            "the available knowledge-base information. "
            "Please consult the relevant approved documentation."
        )
    }

def route_after_decision(state : ClaimValidationState):
    if state["validation_status"]=="VALID":
        return "return_original"

    if state["retry_count"] < state["max_retries"]:
        return "revise"

    return "fallback"

# def route_after_revalidation(state : ClaimValidationState):
#     if state["validation_status"]=="VALID":
#         return "return_revised"

#     return "fallback"

def return_original_node(state : ClaimValidationState):
    return {
        "final_answer" : state["answer"]
    }

def return_revised_node(state : ClaimValidationState):
    return {
        "final_answer" : state["revised_answer"]
    }

def simulated_failed_revision_node(state: ClaimValidationState):
    print("\nSimulating regeneration with an unsupported claim...")

    return {
        "answer": (
            "Application health checks, functional testing, "
            "monitoring and database backup restoration "
            "must be performed after production changes."
        ),
        "retry_count": state["retry_count"] + 1
    }

workflow=StateGraph(ClaimValidationState)

workflow.add_node("extract_claims",claim_extraction_node)
workflow.add_node("verify_claims",verify_claims_node)
workflow.add_node("decide_claims",decide_claims_node)
workflow.add_node("revise_answer",revise_answer_node)
#workflow.add_node("revalidate_answer",revalidate_answer_node)
workflow.add_node("fallback",fallback_node)
workflow.add_node("return_original",return_original_node)
workflow.add_node("return_revised",return_revised_node)

workflow.add_edge(START,"extract_claims")
workflow.add_edge("extract_claims","verify_claims")
workflow.add_edge("verify_claims","decide_claims")

workflow.add_conditional_edges(
    "decide_claims",
    route_after_decision,
    {
        "return_original" : "return_original",
        "revise" : "revise_answer",
        "fallback" : "fallback"
    }
)

workflow.add_edge("revise_answer","extract_claims")
# workflow.add_conditional_edges(
#     "revalidate_answer",
#     route_after_revalidation,
#     {
#         "return_revised" : "return_revised",
#         "fallback" : "fallback"
#     }
# )

workflow.add_edge("return_original",END)
workflow.add_edge("return_revised",END)
workflow.add_edge("fallback",END)

app=workflow.compile()

print("\nClaim level validation Langgraph workflow created successfully")




##############################################
#Retry exhaust workflow
test_workflow = StateGraph(ClaimValidationState)

test_workflow.add_node("extract_claims", claim_extraction_node)
test_workflow.add_node("verify_claims", verify_claims_node)
test_workflow.add_node("decide_claims", decide_claims_node)
test_workflow.add_node("simulate_revision", simulated_failed_revision_node)
test_workflow.add_node("fallback", fallback_node)

test_workflow.add_edge(START, "extract_claims")
test_workflow.add_edge("extract_claims", "verify_claims")
test_workflow.add_edge("verify_claims", "decide_claims")

test_workflow.add_conditional_edges(
    "decide_claims",
    route_after_decision,
    {
        "return_original": END,
        "revise": "simulate_revision",
        "fallback": "fallback"
    }
)

test_workflow.add_edge("simulate_revision", "extract_claims")
test_workflow.add_edge("fallback", END)

retry_test_app = test_workflow.compile()

if __name__=="__main__":
    test_cases=[
        {
            "name": "Mixed claims test",
            "question": "What activities should be performed after a production change?",
            "context": """
            Source: production_validation

            Production changes require application health checks,
            functional testing, monitoring and log verification.
            """,
            "answer": """
            Application health checks, functional testing,
            monitoring and database backup restoration must
            be performed after production changes.
            """
        },
        {
            "name": "All supported claims test",
            "question": "What activities should be performed after a production change?",
            "context": """
            Source: production_validation

            Production changes require application health checks,
            functional testing, monitoring and log verification.
            """,
            "answer": """
            Application health checks, functional testing,
            monitoring and log verification must be performed.
            """
        },
        {
        "name": "Retry exhaustion test",
        "question": "What activities should be performed after a production change?",
        "context": """
        Source: production_validation

        Production changes require application health checks,
        functional testing, monitoring and log verification.
        """,
        "answer": """
        Application health checks, functional testing,
        monitoring and database backup restoration must
        be performed after production changes.
        """
        }
    ]

    for test in test_cases:
        print("\n==========================")
        print(test["name"])
        print("============================")

        initial_state={
            "question" : test["question"],
            "context" : test["context"],
            "answer" : test["answer"],
            "claims": [],
            "verification_results" : [],
            "revised_answer" : "",
            "retry_count" : 0,
            "max_retries" : 3,
            "final_answer" : "",
            "validation_status" : ""
        }

        result=app.invoke(initial_state)

        print("\n========= Final execution result =============")
        print("Validation status : ", result["validation_status"])
        print("Final answer : ")
        print(result["final_answer"])


    print("\n========== RETRY EXHAUSTION TEST ==========")

    retry_test_state = {
        "question": "What activities should be performed after a production change?",
        "context": """
        Source: production_validation

        Production changes require application health checks,
        functional testing, monitoring and log verification.
        """,
        "answer": """
        Application health checks, functional testing,
        monitoring and database backup restoration must
        be performed after production changes.
        """,
        "claims": [],
        "verification_results": [],
        "revised_answer": "",
        "retry_count": 0,
        "max_retries": 3,
        "final_answer": "",
        "validation_status": ""
    }

    retry_result = retry_test_app.invoke(retry_test_state)

    print("\nFinal retry count:", retry_result["retry_count"])
    print("Final validation status:", retry_result["validation_status"])
    print("Final answer:", retry_result["final_answer"])

