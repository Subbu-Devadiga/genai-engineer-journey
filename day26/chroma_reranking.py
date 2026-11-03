from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from sentence_transformers import CrossEncoder

load_dotenv()

embeddings=OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vectorstore=Chroma(
    collection_name="Change_management",
    embedding_function=embeddings,
    persist_directory="../day08/chroma_db"
)

reranker=CrossEncoder(
        "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

query="How do I recover after a failed deployment?"

expected_sources = [
    "rollback",
    "resolution_and_recovery",
    "investigation_and_diagnosis"
]

def evaluate_retrieval(results,expected_sources,k=3):
    retrieved_sources=[
        doc.metadata.get("source") for doc in results[:k]
    ]
    relevant= len(set(retrieved_sources) & set(expected_sources))

    precision= relevant/k
    recall=relevant/len(expected_sources)

    return precision,recall

retrieved_docs=vectorstore.similarity_search(
    query,
    k=10
)

print("\n===== INITIAL VECTOR SEARCH =====")

for rank,doc in enumerate(retrieved_docs,1):
    print(f"\nRank : {rank}")
    print("source :",doc.metadata.get("source"))
    print("content : ",doc.page_content[:200])

pairs=[[query, doc.page_content] for doc in retrieved_docs]

scores= reranker.predict(pairs)

ranked_docs= list(zip(retrieved_docs, scores))

ranked_docs.sort(
    key=lambda x: float(x[1]),
    reverse=True
)

print("\n===== CROSS-ENCODER RERANKED RESULTS =====")

# Step 10: Display final top 3
for rank, (doc, score) in enumerate(ranked_docs[:3], 1):

    print(f"\nRank: {rank}")
    print("Source:", doc.metadata.get("source"))
    print("Relevance Score:", round(float(score), 4))
    print("Content:", doc.page_content[:250])

#Evaluate initial vector search
initial_precision,initial_recall=evaluate_retrieval(
    retrieved_docs,
    expected_sources,
    k=3
)

#Evaluate cross-encoder reranked results
reranked_doc=[doc for doc,score in ranked_docs]
final_precision,final_recall=evaluate_retrieval(
    reranked_doc,
    expected_sources,
    k=3
)

print("\n===== RETRIEVAL EVALUATION =====")

print(
    f"Initial vector search | "
    f"Precision@3 : {initial_precision:.2f} |"
    f"Recall@3 : {initial_recall:.2f}"
)

print(
    f"Cross_encoder reranked |"
    f"Precision@3 : {final_precision:.2f} |"
    f"Recall@3 : {final_recall:.2f}"
)

