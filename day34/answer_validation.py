from typing import TypedDict
import os
from dotenv import load_dotenv
from pydantic import BaseModel,Field

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph,START,END

load_dotenv("../.env")

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OpenAI API key not found...")


class RAGState(TypedDict):
    question : str
    context : str
    answer : str
    validation_status : str
    validation_reason : str
    final_answer : str

class validationResult(BaseModel):
    validation_status : str =Field(
        description="Must be VALID or INVALID"
    )

    validation_reason : str = Field(
        description="Explain why the answer passed or failed validation"
    )

llm=ChatOpenAI(
    model="gpt-6-astra",
    temperature=1
)

structured_llm=llm.with_structured_output(validationResult)

validation_prompt=ChatPromptTemplate.from_template("""
You are an answer validation expert for an enterprise RAG system.

Evaluate the generated answer using ONLY the provided context.

Validation rules:
1. Check every factual claim in the answer.
2. Every factual claim must be supported by the context.
3. Verify that each cited source supports its associated claim.
4. Do not approve unsupported assumptions or invented details.
5. If even one important factual claim is unsupported,
   mark the answer INVALID.
6. Return VALID only when all factual claims are supported.

Question:
{question}

Retrieved Context:
{context}

Generated Answer:
{answer}

Return the validation status and a clear reason.
""")

validation_chain=validation_prompt | structured_llm


def answer_validation_node(state : RAGState):
    print("Validating generated answer.........")

    result=validation_chain.invoke({
        "question" : state["question"],
        "context" : state["context"],
        "answer" : state["answer"]
    })

    print("\nvalidation status : ", result.validation_status)
    print("validation reason : ",result.validation_reason)

    return {
        "validation_status" : result.validation_status,
        "validation_reason" : result.validation_reason
    }

def route_validation(state: RAGState):

    print("DEBUG - Validation state:", state)
    print("DEBUG - Status value:", repr(state["validation_status"]))

    if state["validation_status"] == "VALID":
        print("Validation passed. Returning answer...")
        return "return_answer"

    else:
        print("Validation failed. Executing safe fallback...")
        return "fallback"

def return_answer_node(state:RAGState):

    return {
        "final_answer" : state["answer"]
    }

def fallback_node(state:RAGState):
    return {
        "final_answer" : (
            "I cannot provide a reliable answer because "
            "the generated response contains claims that "
            "are not sufficiently supported by the "
            "knowledge base. Please consult the relevant "
            "approved documentation."
        )
    }

workflow=StateGraph(RAGState)

workflow.add_node("validate_answer",answer_validation_node)
workflow.add_node("return_answer",return_answer_node)
workflow.add_node("fallback",fallback_node)

workflow.add_edge(START,"validate_answer")
workflow.add_conditional_edges(
    "validate_answer",
    route_validation,
    {
        "return_answer" : "return_answer",
        "fallback" : "fallback"
    }
)

workflow.add_edge("return_answer",END)
workflow.add_edge("fallback",END)

app=workflow.compile()

print("Answer validation langgraph workflow created successfully.....")


if __name__=="__main__":
    test_cases=[
        {
            "name": "Valid answer test",
            "question": "What activities should be performed after a production change?",
            "context": """
            Source: production_validation
            Production changes require application health checks,
            functional testing, monitoring and log verification.
            """,
            "answer": """
            Application health checks, functional testing,
            monitoring and log verification.
            [Source: production_validation]
            """
        },
        {
            "name": "Invalid answer test",
            "question": "What activities should be performed after a production change?",
            "context": """
            Source: production_validation
            Production changes require application health checks,
            functional testing, monitoring and log verification.
            """,
            "answer": """
            Application health checks, functional testing,
            monitoring, log verification and database backup
            restoration.
            [Source: production_validation]
            """
        }
        ]


    for test in test_cases:
        print("=================================")
        print(test["name"])
        print("=================================")

        initial_state={
            "question" : test["question"],
            "context" : test["context"],
            "answer" : test["answer"],
            "validation_status" : "",
            "validation_reason" : "",
            "final_answer": ""
        }

        result=app.invoke(initial_state)

        print("\nFinal execution result")
        print("Validation status : ", result["validation_status"])
        print("Final answer : ", result["final_answer"])