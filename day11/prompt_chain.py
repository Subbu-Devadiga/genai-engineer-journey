from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

model=ChatOpenAI(
    model="gpt-6-astra"
)

prompt=ChatPromptTemplate.from_messages(
     [
        (
            "system",
            "You are an enterprise IT Change Management assistant."
        ),
        (
            "human",
            "Explain the following change type: {change_type}"
        )
    ]
)

chain= prompt | model

response=chain.invoke(
    {
        "change_type": "Emergency Change"
    }
)

print(response.content)