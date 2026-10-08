from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

model=ChatOpenAI(
    model="gpt-6-astra"
)

response=model.invoke(
    "Explain what an emergency change is in IT change management."
)

print(response.content)