from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

import re
from rank_bm25 import BM25Okapi

load_dotenv()

embeddings=OpenAIEmbeddings(model="text-embedding-3-small")

vectorstore=Chroma(
    collection_name="Change_management",
    embedding_function=embeddings,
    persist_directory="../day08/chroma_db"
)

stored_data=vectorstore.get()

documents=stored_data["documents"]
metadatas=stored_data["metadatas"]
ids=stored_data["ids"]

for i in range(min(5,len(documents))):
    print("\nDocument ID:", ids[i])
    print("Source:", metadatas[i].get("source"))
    print("Content:", documents[i][:200])


def tokenizer(text):
    return re.findall(r"[a-z0-9]+",text.lower())

tokenized_documents=[tokenizer(doc) for doc in documents]

bm25=BM25Okapi(tokenized_documents)

def bm25_search(query,top_k=3):
    query_tokens=tokenizer(query)

    scores=bm25.get_scores(query_tokens)

    ranked_indices=sorted(
        range(len(scores)),
        key=lambda i:scores[i],
        reverse=True
    )

    results=[]

    for index in ranked_indices[:top_k]:
        if scores[index]>0:
            results.append({
                "id" : ids[index],
                "source" : metadatas[index].get("source"),
                "content" : documents[index],
                "score" : float(scores[index])
            })
        if len(results)==top_k:
            break

    return results

def vector_search(query, top_k=3):

    search_results = vectorstore.similarity_search(
        query,
        k=top_k
    )

    results = []

    for doc in search_results:

        results.append({
            "id": doc.metadata.get("source"),
            "source": doc.metadata.get("source"),
            "content": doc.page_content
        })

    return results

def reciprocal_rank_fusion(
    bm25_results,
    vector_results,
    k=60
):

    rrf_scores = {}
    documents_map = {}

    retrieval_lists = [
        bm25_results,
        vector_results
    ]

    for results in retrieval_lists:

        for rank, result in enumerate(results, 1):

            doc_id = result["id"]

            score = 1 / (k + rank)

            rrf_scores[doc_id] = (
                rrf_scores.get(doc_id, 0) + score
            )

            documents_map[doc_id] = result

    ranked_documents = sorted(
        rrf_scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    final_results = []

    for doc_id, score in ranked_documents:

        result = documents_map[doc_id].copy()

        result["rrf_score"] = score

        final_results.append(result)

    return final_results

def evaluate_retrieval(results, expected_sources, k=3):

    retrieved_sources = [
        result["source"]
        for result in results[:k]
    ]

    relevant_retrieved = len(
        set(retrieved_sources) & set(expected_sources)
    )

    precision = relevant_retrieved / k

    recall = (
        relevant_retrieved / len(expected_sources)
        if expected_sources else 0
    )

    return precision, recall

if __name__ == "__main__":

    questions = [
        "What is a rollback plan?",
        "What should I consider before implementing a production change?",
        "How do I recover after a failed deployment?"
    ]

    for question in questions:
        expected_results = {
    "What is a rollback plan?": [
        "rollback"
    ],

    "What should I consider before implementing a production change?": [
        "normal_change",
        "production_validation",
        "cab"
    ],

    "How do I recover after a failed deployment?": [
        "rollback",
        "deployment_strategy",
        "resolution_and_recovery"
    ]
}

        print("\n" + "=" * 70)
        print("QUESTION:", question)
        print("=" * 70)

        # BM25 retrieval
        bm25_results = bm25_search(question, top_k=3)

        # Vector retrieval
        vector_results = vector_search(question, top_k=3)

        # Hybrid retrieval using RRF
        hybrid_results = reciprocal_rank_fusion(
            bm25_results,
            vector_results,
            k=60
        )

        print("\n===== BM25 SEARCH =====")

        for rank, result in enumerate(bm25_results, 1):
            print(f"Rank: {rank} | Source: {result['source']}")

        print("\n===== VECTOR SEARCH =====")

        for rank, result in enumerate(vector_results, 1):
            print(f"Rank: {rank} | Source: {result['source']}")

        print("\n===== HYBRID SEARCH (RRF) =====")

        for rank, result in enumerate(hybrid_results[:3], 1):
            print(
                f"Rank: {rank} | "
                f"Source: {result['source']} | "
                f"RRF Score: {result['rrf_score']:.6f}"
            )

        expected = expected_results[question]

        bm25_p, bm25_r = evaluate_retrieval(
    bm25_results, expected
)

        vector_p, vector_r = evaluate_retrieval(
            vector_results, expected
    )

        hybrid_p, hybrid_r = evaluate_retrieval(
            hybrid_results, expected
)

        print("\n===== RETRIEVAL EVALUATION =====")

        print(
    f"BM25     | Precision@3: {bm25_p:.2f} "
    f"| Recall@3: {bm25_r:.2f}"
)

        print(
    f"Vector   | Precision@3: {vector_p:.2f} "
    f"| Recall@3: {vector_r:.2f}"
)

        print(
    f"Hybrid   | Precision@3: {hybrid_p:.2f} "
    f"| Recall@3: {hybrid_r:.2f}"
)