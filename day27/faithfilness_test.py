from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from ragas.llms import LangchainLLMWrapper
from ragas import evaluate
from ragas.metrics import Faithfulness

from rag_evaluation import dataset

load_dotenv("../.env")

llm=ChatOpenAI(
    model="gpt-6-astra",
    temperature=1
)

evaluator_llm=LangchainLLMWrapper(llm,bypass_temperature=True)

faithfulness=Faithfulness(llm=evaluator_llm)

result=evaluate(dataset,
                metrics=[faithfulness]
                )

print("\n===== FAITHFULNESS EVALUATION =====")
print(result)