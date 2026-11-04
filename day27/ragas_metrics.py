import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from  ragas.llms import LangchainLLMWrapper

load_dotenv("../.env")

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

llm=ChatOpenAI(
    model="gpt-6-astra"
)

evaluator_llm=LangchainLLMWrapper(llm)

print("OpenAI evaluator configured successfully")