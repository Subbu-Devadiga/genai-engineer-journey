from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from ragas import evaluate
from ragas.metrics import LLMContextPrecisionWithReference
from ragas.llms import LangchainLLMWrapper
from rag_evaluation import dataset

load_dotenv("../.env")

llm=ChatOpenAI(
    model="gpt-6-astra",
    temperature=1
)

evaluator_llm=LangchainLLMWrapper(
    llm,
    bypass_temperature=True
)
context_precision=LLMContextPrecisionWithReference(llm=evaluator_llm)

result=evaluate(dataset,metrics=[context_precision])

print("\n===== CONTEXT PRECISION EVALUATION =====")
print(result)