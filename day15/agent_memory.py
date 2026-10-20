
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage

from langgraph.graph import StateGraph, START, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()


# 1. Define a change-management tool
@tool
def get_change_requirements(change_type: str) -> str:
    """Retrieve documentation requirements for normal or emergency changes."""

    policies = {
        "normal": (
            "Normal change requirements: documented scope, risk and "
            "impact assessment, test evidence, implementation plan, "
            "rollback plan, and required approvals."
        ),
        "emergency": (
            "Emergency change requirements: documented emergency "
            "justification, risk and impact assessment, implementation "
            "and rollback plans, appropriate emergency authorization, "
            "and retrospective review according to organizational policy."
        ),
    }

    key = change_type.strip().lower()

    return policies.get(
        key,
        "Unsupported change type. Available categories: normal, emergency."
    )


tools = [get_change_requirements]

model = ChatOpenAI(model="gpt-6-astra")
model_with_tools = model.bind_tools(tools)


# 2. Define the LLM node
def chatbot(state: MessagesState):
    response = model_with_tools.invoke(state["messages"])
    return {"messages": [response]}


# 3. Build the graph
builder = StateGraph(MessagesState)

builder.add_node("chatbot", chatbot)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "chatbot")
builder.add_conditional_edges("chatbot", tools_condition)
builder.add_edge("tools", "chatbot")


# 4. Add an in-memory checkpointer
memory = InMemorySaver()
graph = builder.compile(checkpointer=memory)


# 5. Use the same thread ID for related conversation turns
config = {
    "configurable": {
        "thread_id": "change-management-demo"
    }
}

if __name__ == "__main__":
    # First interaction
    print("\n--- Turn 1 ---")

    result1 = graph.invoke(
        {
            "messages": [
                SystemMessage(
                    content=(
                        "You are an IT change management assistant. "
                        "Use the policy tool for documentation requirements. "
                        "Use previous conversation context when relevant. "
                        "Do not claim to approve changes."
                    )
                ),
                HumanMessage(
                    content=(
                        "What documentation is required for an "
                        "emergency change?"
                    )
                ),
            ]
        },
        config=config,
    )

    print(result1["messages"][-1].content)

    # Second interaction: refers to the previous conversation
    print("\n--- Turn 2 ---")

    result2 = graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content="What about a normal change?"
                ),
            ]
        },
        config=config,
    )

    print(result2["messages"][-1].content)

    # 6. Inspect the saved conversation state
    snapshot = graph.get_state(config)

    print("\n--- Saved Conversation State ---")
    print("Messages stored:", len(snapshot.values["messages"]))

    for message in snapshot.values["messages"]:
        print(type(message).__name__)

    # 7. Start a separate conversation
    new_config = {
        "configurable": {
            "thread_id": "separate-demo"
        }
    }

    result3 = graph.invoke(
        {
            "messages": [
                SystemMessage(
                    content=(
                    "You are an IT change management assistant. "
                    "Use the policy tool for documentation requirements. "
                    "Do not invent policy."
                    )
                ),
                HumanMessage(
                    content="What about the other change type?"
                ),
            ]
        },
        config=new_config,
    )

    print("\n--- Separate Conversation ---")
    print(result3["messages"][-1].content)
