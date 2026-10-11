from typing import TypedDict,Literal
from pydantic import BaseModel,Field
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph,START,END

load_dotenv()

#1. Define the structured response expected from LLM
class ChangeAnalysis(BaseModel):
    risk_level : Literal['high','medium','low']=Field(
        description="The assessed risk level of the change"
    )

    rationale :str=Field(
        description="Explain main factors behind risk assessment"
    )

#2. Define workflow state
class ChangeState(TypedDict):
    change_description : str
    risk_level : str
    rationale : str
    decision : str


#3. Configure the LLM with structured output
model=ChatOpenAI(
    model="gpt-6-astra"
    #temperature=0
)

structured_model=model.with_structured_output(ChangeAnalysis)

#4. LLM mode analyze change
def analyze_change(state : ChangeState):
    result=structured_model.invoke([
        (
            "system",
            """
            You are assisting an enterprise IT change management team.

            Classify the potential risk of the change as low, medium,
            or high. Consider production impact, database changes,
            service disruption, scope, and potential business impact.

            Explain your reasoning briefly.

            This is a preliminary assessment, not an official
            risk decision or change approval.
            """
        ),
        (
            "human",
            f"Analyze this change: {state['change_description']}"
        )
    ])

    print("\nLLM risk assessment:", result.risk_level)
    print("Rationale:", result.rationale)

    return {
        "risk_level": result.risk_level,
        "rationale": result.rationale
    }

#5 define conditional routing
def route_change(state: ChangeState):
    if state["risk_level"]=="high":
        return "enhanced_review"

    return "standard_review"

#6. Define the workflow branches

def enhanced_review(state:ChangeState):
    return {
        "decision": "Enhanced review required; human review required"
    }

def standard_review(state: ChangeState):
    return {
        "decision" : "Standard review required; approval still required"
    }

#7.Build the graph

builder=StateGraph(ChangeState)

builder.add_node("analyze_change",analyze_change)
builder.add_node("enhanced_review",enhanced_review)
builder.add_node("standard_review",standard_review)

builder.add_edge(START,"analyze_change")
builder.add_conditional_edges(
    "analyze_change",
    route_change,
    {
        "enhanced_review" : "enhanced_review",
        "standard_review" : "standard_review"
    }
)

builder.add_edge("enhanced_review",END)
builder.add_edge("standard_review",END)

#8. compile the graph
graph=builder.compile()

#9 Test the workflow
if __name__=="__main__":
    test_change=(
        #"Modify the production database schema for the "
        #"Modify the production database schema for the customer payment service."
        #"Update the documentation on an internal development environment."
        "Upgrade the production payment gateway with a planned service interruption."
        #"customer payment service."
    )

    result=graph.invoke({
        "change_description" : test_change,
        "risk_level": "",
        "rationale" : "",
        "decision" : "",

    })

    print("\n--- Final Workflow Result ---")
    print("\n",result)