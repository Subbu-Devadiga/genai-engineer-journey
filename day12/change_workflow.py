from typing import TypedDict
from langgraph.graph import StateGraph,START,END

class ChangeState(TypedDict):
    change_description : str
    risk : str
    decision : str

def analyze_change(state : ChangeState):
    description= state['change_description'].lower()

    if "production database" in description:
        risk="high"

    elif "production" in description:
        risk="medium"

    else:
        risk="low"

    return {
        "risk" : risk
    }

def route_change(state : ChangeState):
    if state["risk"]=="high":
        return "cab_review"

    else:
        return "normal_approval"

def cab_review(state : ChangeState):
    return {
        "decision" : "CAB review required"
    }

def normal_approval(state : ChangeState):
    return {
        "decision" : "Normal approval process"
    }

graphbuilder=StateGraph(ChangeState)

graphbuilder.add_node("analyze_change",analyze_change)
graphbuilder.add_node("cab_review",cab_review)
graphbuilder.add_node("normal_approval",normal_approval)

graphbuilder.add_edge(START,"analyze_change")

graphbuilder.add_conditional_edges(
    "analyze_change", route_change,
    {
        "cab_review":"cab_review",
        "normal_approval" : "normal_approval"
    }
)

graphbuilder.add_edge("cab_review",END)
graphbuilder.add_edge("normal_approval",END)

graph=graphbuilder.compile()

result = graph.invoke(
    {
        "change_description":
            "Update development application configuration",
        "risk": "",
        "decision": ""
    }
)


print(result)