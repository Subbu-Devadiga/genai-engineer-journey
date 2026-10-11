from typing import TypedDict

from langgraph.graph import StateGraph,START,END

class State(TypedDict):
    message : str

def greet(state : State):
    return {
        "message" : f"Hello, {state["message"]}!"
        }
    

graphbuilder=StateGraph(State)

graphbuilder.add_node("greet",greet)
graphbuilder.add_edge(START,"greet")
graphbuilder.add_edge("greet",END)

graph=graphbuilder.compile()

result=graph.invoke(
    {"message" : "GenAI Engineer"}
)

print(result)