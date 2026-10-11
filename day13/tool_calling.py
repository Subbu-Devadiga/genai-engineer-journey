from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    ToolMessage
)

load_dotenv()

#1. Define python function as an llm tool
@tool
def get_change_requirements(change_type : str) -> str:
    """Return the required documentation for a normal or emergency IT change."""

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
    key=change_type.strip().lower()

    return policies.get(
        key,
        "Unknown change type. Please specify normal or emergency."
    )

#2. Configure the model and make tool available for it
model= ChatOpenAI(model="gpt-6-astra")

tools=[get_change_requirements]
tool_map={item.name:item for item in tools}

model_with_tools=model.bind_tools(tools)

#3. Start conversation
messages=[SystemMessage(
    content=(
            "You are an IT change management assistant. "
            "Use the get_change_requirements tool when the user "
            "asks about required change documentation. "
            "Clearly distinguish retrieved policy information "
            "from assumptions. Do not claim to approve changes."
    )
),
HumanMessage(
    content="What is the process for a standard database change?"
)
]

response=model_with_tools.invoke(messages)

while response.tool_calls:
    messages.append(response)

    for tool_call in response.tool_calls:
        tool_name=tool_call["name"]
        tool_args=tool_call["args"]

        print(f"\nTool requested: {tool_name}")
        print(f"Tool arguments: {tool_args}")

        selected_tool=tool_map[tool_name]
        tool_result=selected_tool.invoke(tool_args)

        print(f"Tool result: {tool_result}")

        messages.append(
            ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_call["id"]
            )
        )

        response = model_with_tools.invoke(messages)


# 6. Display the final answer
print(f"\n--- Final Answer ---")
print(response.content)