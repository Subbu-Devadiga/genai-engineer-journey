from typing import TypedDict,Literal
from langgraph.graph import StateGraph,START,END

class validationState(TypedDict):
    question : str
    context : str
    answer : str
    status : str
    final_answer : str


def validate_answer(state : validationState):
    context=state['context'].strip()
    answer=state['answer'].strip()

    if not context:
        return {
            "status" : "rejected",
            "final_answer" : (
                "I cannot provide a reliable answer because "
                "no supporting information was retrieved."
            ),
        }

    if not answer:
        return {
            "status" : "rejected",
            "final_answer" :"No answer was generated. Please try again.",
        }

    return {
        "status" : "passed_basic_checks",
        "final_answer" : answer,
    }

def route_after_validation(
    state: validationState,
) -> Literal["approved", "fallback"]:
    
    if state["status"]=="passed_basic_checks":
        return "approved"

    return "fallback"

def approved(state : validationState):
    return {
        "final_answer" : state["final_answer"],
        "status" : "Approved_basic_checks"
    }

def fallback(state : validationState):
    return {
        "final_answer" : (
            "Insufficient information: I cannot provide a "
            "reliable answer because supporting context or "
            "a usable answer is missing."
        ),
        "status": "rejected",
    }
builder=StateGraph(validationState)

builder.add_node("validate_answer",validate_answer)
builder.add_node("approved",approved)
builder.add_node("fallback",fallback)

builder.add_edge(START,"validate_answer")
builder.add_conditional_edges(
    "validate_answer",
    route_after_validation,
    {
        "approved" : "approved",
        "fallback" : "fallback",
    },
    )
builder.add_edge("approved",END)
builder.add_edge("fallback",END)

graph=builder.compile()


if __name__=="__main__":
    test_case=[
        {
            "question" : "What is a rollback plan?",
            "context" : (
                "A rollback plan describes how to restore "
                "the previous working state if a change fails."
            ),
            "answer" : ("A rollback plan explains how to restore "
                "the previous working state if a change fails."
            ),
        },
        {
            "question" : "What is the maximum number of CAB members?",
            "context" : "",
            'answer' : "The maximum is 15 members.",
        },
        {
            "question" : "What is a rollback plan?",
            "context" : "A rollback plan restores a previous state.",
            "answer" : "",
        }
    ]

    for index,case in enumerate(test_case, start=1):
        result=graph.invoke({
            **case,
            "status" : "",
            "final_answer": "",
        })

        print(f"\n--- Test Case {index} ---")
        print("\nQuestion:", result["question"])
        print("Validation:", result["status"])
        print("Final answer:", result["final_answer"])
