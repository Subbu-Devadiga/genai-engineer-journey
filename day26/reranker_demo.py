from sentence_transformers import CrossEncoder

model= CrossEncoder(
        "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

query="How do I recover after a failed deployment?"

documents=[
    {
        "source": "deployment_strategy",
        "content": "Deployment strategy defines the sequence "
                   "and approach for deploying software into production."
    },
    {
        "source": "rollback",
        "content": "A rollback procedure describes how to restore "
                   "the previous stable state if a deployment fails."
    },
    {
        "source": "change_closure",
        "content": "After successful implementation, changes "
                   "should be reviewed and formally closed."
    },
    {
        "source": "resolution_and_recovery",
        "content": "Recovery procedures help restore affected "
                   "services after deployment failures."
    }
]

pairs=[[query,doc["content"]] for doc in documents]

scores=model.predict(pairs)

for doc,score in zip(documents,scores):
    doc["score"]=float(score)


ranked_documents= sorted(
    documents,
    key=lambda x: x["score"],
    reverse=True
)

print("\n===== CROSS-ENCODER RERANKING =====")

print("Question :", query)

for rank,doc in enumerate(ranked_documents,1):
    print("Rank :", rank)
    print("Source:", doc["source"])
    print("Relevance Score:", round(doc["score"], 4))
    print("Content:", doc["content"])