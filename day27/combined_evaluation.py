from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from ragas import evaluate
from ragas.llms import LangchainLLMWrapper
from rag_evaluation import dataset
from ragas.metrics import (
    Faithfulness,
    AnswerRelevancy,
    LLMContextPrecisionWithReference,
    LLMContextRecall
)

load_dotenv("../.env")

llm=ChatOpenAI(model="gpt-6-astra",temperature=1)

evaluator_llm=LangchainLLMWrapper(llm,bypass_temperature=True)

metrics=[
    Faithfulness(llm=evaluator_llm),
    AnswerRelevancy(llm=evaluator_llm),
    LLMContextPrecisionWithReference(llm=evaluator_llm),
    LLMContextRecall(llm=evaluator_llm)
]

result=evaluate(dataset,metrics=metrics)

print("\n===== COMBINED RAG EVALUATION =====")

print(result)
print("\n===== INDIVIDUAL METRIC SCORES =====")

scores = result.to_pandas()

for column in scores.columns:
    if column in [
        "faithfulness",
        "answer_relevancy",
        "llm_context_precision_with_reference",
        "context_recall"
    ]:
        print(f"{column}: {scores[column].mean():.4f}")