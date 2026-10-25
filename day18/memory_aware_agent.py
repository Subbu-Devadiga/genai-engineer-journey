from dotenv import load_dotenv
from typing import TypedDict
from langchain_openai import ChatOpenAI

from langchain_core.messages import HumanMessage,SystemMessage
from langgraph.graph import StateGraph,START,END
from langgraph.store.memory import InMemoryStore

load_dotenv()

# 1. Define the workflow state
class AgentState(TypedDict):
    question : str
    memory_context :str
    answer : str

store=InMemoryStore()

namespace=("Change_management","demo_user001")

store.put(
    namespace,
    "Environment_preferences",
    {
        "preferred_environment": "UAT",
        "application": "Customer Payment Service",
    },
)

store.put(
    namespace,
    "response_preferences",
    {
        "response_style": "Short bullet points",
        "detail_level": "Detailed",
    },
)

model=ChatOpenAI(model="gpt-6-astra")

def retrieve_memory(state : AgentState):
    memories = store.search(namespace)

    if not memories:
        return {"memory_context": "No saved preferences are available."}

    memory_lines = []

    for item in memories:
        memory_lines.append(
            f"{item.key}: {item.value}"
        )

    return {
        "memory_context": "\n".join(memory_lines)
    }


def chatbot(state : AgentState):
    messages=[
        SystemMessage(
            content=(
                "You are an enterprise IT change management assistant. "
                "Use saved memory only to personalize the answer, such as "
                "its format or relevant environment. Memory preferences "
                "are not official policies. Never invent policy requirements "
                "or claim that a change is approved."
            )
        ),
        HumanMessage(
            content=(
                f"Saved user preferences:\n{state['memory_context']}\n\n"
                f"User question:\n{state['question']}\n\n"
                "Use relevant preferences where appropriate. If a preference "
                "is unrelated to the question, ignore it."

            )
        ),
    ]

    response = model.invoke(messages)

    content=response.content

    if isinstance(content,list):
        text_parts=[]

        for block in content:
            if isinstance(block,dict) or block.get("type")=="text":
                text_parts.append(block.get("text", ""))

            elif hasattr(block,"text"):
                text_parts.append(block.text)
        content="\n".join(text_parts)

    return {"answer" : content}

builder = StateGraph(AgentState)

builder.add_node("retrieve_memory", retrieve_memory)
builder.add_node("chatbot", chatbot)

builder.add_edge(START, "retrieve_memory")
builder.add_edge("retrieve_memory", "chatbot")
builder.add_edge("chatbot", END)

graph = builder.compile()


# 7. Run the agent
if __name__ == "__main__":
    question = input("Ask a change-management question: ").strip()

    if not question:
        print("Please enter a question.")
    else:
        result = graph.invoke(
            {
                "question": question,
                "memory_context": "",
                "answer": "",
            }
        )

        print("\n--- Retrieved Memory ---")
        print(result["memory_context"])

        print("\n--- Agent Answer ---")
        print(result["answer"])

