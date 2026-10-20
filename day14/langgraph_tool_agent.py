from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage

from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()


# 1. Define a tool
@tool
def get_change_requirements(change_type: str) -> str:
    """Retrieve predefined documentation requirements for a normal or emergency IT change."""

    policies = {
        "normal": (
            "Normal change requirements: documented scope, "
            "risk and impact assessment, test evidence, "
            "implementation plan, rollback plan, and required approvals."
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


# 2. Configure the model with the available tools
model = ChatOpenAI(model="gpt-6-astra")
model_with_tools = model.bind_tools(tools)


# 3. Define the LLM node
def chatbot(state: MessagesState):
    response = model_with_tools.invoke(state["messages"])
    return {"messages": [response]}


# 4. Build the graph
builder = StateGraph(MessagesState)

builder.add_node("chatbot", chatbot)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "chatbot")

# Route to tools if the model requested a tool call.
# Otherwise, finish the graph.
builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)

# After executing a tool, return to the LLM.
builder.add_edge("tools", "chatbot")

graph = builder.compile()


# 5. Run the agent
if __name__ == "__main__":
    messages = [
        SystemMessage(
            content=(
                "You are an IT change management assistant. "
                "Use get_change_requirements for questions about "
                "normal or emergency change documentation. "
                "Base policy-specific claims on the tool result. "
                "If the tool reports an unsupported category, explain "
                "the limitation rather than inventing a policy. "
                "Do not claim to approve changes."
            )
        ),
        HumanMessage(
            content="What is an AI agent in simple terms?"
        ),
    ]

    result = graph.invoke({"messages": messages})

    print("\n--- Conversation Trace ---")

    for message in result["messages"]:
        print(f"\nMessage type: {type(message).__name__}")

        if getattr(message, "tool_calls", None):
            print("Tool calls:", message.tool_calls)

        if message.type == "tool":
            print("Tool result:", message.content)

    print("\n--- Final Answer ---")
    print(result["messages"][-1].content)
