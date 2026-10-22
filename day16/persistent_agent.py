from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage,SystemMessage

from langgraph.graph import StateGraph,START,MessagesState
from langgraph.prebuilt import ToolNode,tools_condition
from langgraph.checkpoint.sqlite import SqliteSaver

load_dotenv()

@tool
def get_change_requirements(change_type : str) ->str:
    """Retrieve documentation requirements for normal or emergency changes."""
    policies={
        "normal" : (
            "Normal change requirements: documented scope, risk and "
            "impact assessment, test evidence, implementation plan, "
            "rollback plan, and required approvals."
        ),
        "emergency" : (
            "Emergency change requirements: documented emergency "
            "justification, risk and impact assessment, implementation "
            "and rollback plans, appropriate emergency authorization, "
            "and retrospective review according to organizational policy."
        ),
    }

    key=change_type.strip().lower()

    return policies.get(
        key,
        "Unsupported change type. Available categories: normal, emergency."
    )

tools=[get_change_requirements]

model=ChatOpenAI(model="gpt-6-astra")
model_with_tools=model.bind_tools(tools)

def chatbot(state: MessagesState):
    response=model_with_tools.invoke(state["messages"])
    return {"messages" : [response]}

builder=StateGraph(MessagesState)
builder.add_node("chatbot",chatbot)
builder.add_node("tools",ToolNode(tools))

builder.add_edge(START,"chatbot")
builder.add_conditional_edges("chatbot",tools_condition)
builder.add_edge("tools","chatbot")

with SqliteSaver.from_conn_string("day16_checkpoints.sqlite") as checkpointer:
    graph=builder.compile(checkpointer=checkpointer)

    config={
        "configurable" : {
            "thread_id" : "change_management_thread_001"
        }
    }

    # Determine whether this thread already has saved messages.
    snapshot=graph.get_state(config)
    saved_messages=snapshot.values.get("messages",[])
    if not saved_messages:
        messages=[
            SystemMessage(
                content=(
                    "You are an IT change management assistant. "
                    "Use the policy tool for documentation requirements. "
                    "Do not invent official policy or claim to approve changes."
                )
            )
        ]

    else:
        messages=[]


    question=input("Ask a change management question : ").strip()

    if not question:
        print("Please enter a question")

    else:
        messages.append(HumanMessage(content=question))

        result=graph.invoke(
            {"messages" : messages},
            config=config,
        )

        print("\n--- Agent Answer ---")
        answer=result["messages"][-1].content

        if isinstance(answer,list):
            for block in answer:
                if isinstance(block,dict) and block.get("type")=="text":
                    print(block.get("text",""))
                elif hasattr(block,"text"):
                    print(block.text)

        else:
            print(answer)

        print("\nConversation messages saved:",
              len(result["messages"]))
