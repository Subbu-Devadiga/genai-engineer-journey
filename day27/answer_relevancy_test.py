from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from ragas import evaluate
from ragas.llms import LangchainLLMWrapper,llm_factory
from ragas.metrics import AnswerRelevancy
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

answer_relevancy=AnswerRelevancy(llm=evaluator_llm)

result=evaluate(dataset, metrics=[answer_relevancy])

print("\n===== ANSWER RELEVANCY EVALUATION =====")
print(result)
