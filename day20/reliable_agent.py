
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    question: str
    answer: str
    evidence: str
    risk_level: str
    status: str
    final_answer: str


def prepare_answer(state: AgentState):
    question = state["question"].lower()

    if "rollback plan" in question:
        answer = (
            "A rollback plan explains how to restore the "
            "previous working state if a change fails."
        )
        evidence = (
            "A rollback plan explains how to restore the "
            "previous working state if a change fails. "
            "It should also define rollback triggers and "
            "validation steps."
        )

    elif "maximum number of cab members" in question:
        answer = "The maximum number is 12."
        evidence = ""

    elif "approve production deployment" in question:
        answer = ""
        evidence = ""

    else:
        answer = ""
        evidence = ""

    return {
        "answer": answer,
        "evidence": evidence,
    }


def validate_answer(state: AgentState):
    answer = state["answer"].strip().lower()
    evidence = state["evidence"].strip().lower()

    if answer and evidence and answer in evidence:
        return {"status": "approved"}

    return {"status": "rejected"}


def assess_risk(state: AgentState):
    question = state["question"].lower()

    high_risk_phrases = [
        "execute",
        "approve",
        "production deployment",
    ]

    if any(phrase in question for phrase in high_risk_phrases):
        return {"risk_level": "high"}

    return {"risk_level": "normal"}


def route_after_checks(
    state: AgentState,
) -> Literal["answer", "fallback", "human_review"]:

    # High-risk requests always require review first.
    if state["risk_level"] == "high":
        return "human_review"

    if state["status"] == "approved":
        return "answer"

    return "fallback"


def return_answer(state: AgentState):
    return {"final_answer": state["answer"]}


def fallback(state: AgentState):
    return {
        "final_answer": (
            "Insufficient information: I cannot provide "
            "a reliable answer from the available evidence."
        )
    }


def human_review(state: AgentState):
    return {
        "final_answer": (
            "Human review required before proceeding. "
            "No production action has been authorized."
        )
    }


builder = StateGraph(AgentState)

builder.add_node("prepare_answer", prepare_answer)
builder.add_node("validate_answer", validate_answer)
builder.add_node("assess_risk", assess_risk)
builder.add_node("return_answer", return_answer)
builder.add_node("fallback", fallback)
builder.add_node("human_review", human_review)

builder.add_edge(START, "prepare_answer")
builder.add_edge("prepare_answer", "validate_answer")
builder.add_edge("validate_answer", "assess_risk")

builder.add_conditional_edges(
    "assess_risk",
    route_after_checks,
    {
        "answer": "return_answer",
        "fallback": "fallback",
        "human_review": "human_review",
    },
)

builder.add_edge("return_answer", END)
builder.add_edge("fallback", END)
builder.add_edge("human_review", END)

app = builder.compile()


if __name__ == "__main__":
    questions = [
        "What is a rollback plan?",
        "What is the maximum number of CAB members?",
        "Approve production deployment",
    ]

    for question in questions:
        result = app.invoke({
            "question": question,
            "answer": "",
            "evidence": "",
            "risk_level": "",
            "status": "",
            "final_answer": "",
        })

        print(f"\nQuestion: {question}")
        print(f"Validation: {result['status']}")
        print(f"Risk: {result['risk_level']}")
        print(f"Final answer: {result['final_answer']}")
