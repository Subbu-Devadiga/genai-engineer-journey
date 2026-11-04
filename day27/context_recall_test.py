from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from ragas import evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import LLMContextRecall
from rag_evaluation import dataset

load_dotenv()

llm=ChatOpenAI(
    model="gpt-6-astra",
    temperature=1
)

evaluator_llm=LangchainLLMWrapper(llm, bypass_temperature=True)

context_recall=LLMContextRecall(llm=evaluator_llm)

result=evaluate(
    dataset,
    metrics=[context_recall]
)
print("\n===== CONTEXT RECALL EVALUATION =====")
print(result)