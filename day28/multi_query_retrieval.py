import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma

load_dotenv("../.env")

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")

embeddings=OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vectorstore=Chroma(
    collection_name="Change_management",
    embedding_function=embeddings,
    persist_directory="../day08/chroma_db"
)
llm=ChatOpenAI(
    model="gpt-6-astra",
    temperature=1
)

prompt= ChatPromptTemplate.from_template(
    """
You are an expert enterprise Change Management assistant.

Generate 3 alternative search queries for the user's question.

Each query should express the same intent using different
terminology or wording.

Return only the 3 queries, one per line.
Do not provide explanations or numbering.

User question: {question}
"""
)

query_generator=prompt | llm

question="How do I recover after a failed production deployment?"
response =query_generator.invoke({
    "question" : question
})

generated_query=response.content.strip().split("\n")

print("--------Original Query---------")
print(question)

print("---------Generated query-------")
for index,query in enumerate(generated_query,start=1):
    print(f"{index} : {query}")


all_queries=[question]+generated_query

all_results=[]
retrieval_result=[]

for query in all_queries:
    print(f"\nSearching for {query}")

    results=vectorstore.similarity_search(
        query,
        k=5
    )

    all_results.extend(results)
    retrieval_result.append(results)

unique_results={}

for doc in all_results:
    unique_results[doc.page_content]=doc

print("\n===== MULTI-QUERY RETRIEVAL RESULTS =====")

for index, doc in enumerate(unique_results.values(), start=1):

    print(f"\nDocument {index}")
    print("Source:", doc.metadata.get("source"))
    print("Content:", doc.page_content[:250])



expected_sources={
    "rollback",
    "resolution_and_recovery",
    "investigation_and_diagnosis"
}

single_results=vectorstore.similarity_search(
    question,
    k=3
)
single_sources={doc.metadata.get("source") for doc in single_results}
multi_sources={doc.metadata.get("source") for doc in unique_results.values()}

def evaluate_retrieval(retrieved_sources):
    relevant=len(retrieved_sources & expected_sources)

    precision=relevant/len(retrieved_sources)
    recall=relevant/len(expected_sources)

    return precision,recall

single_precision,single_recall=evaluate_retrieval(single_sources)
multi_precision,multi_recall=evaluate_retrieval(multi_sources)

print("\n===== RETRIEVAL COMPARISON =====")

print(
    f"Single Query: Precision={single_precision:.2f}, "
    f"Recall={single_recall:.2f}"
)

print(
    f"Multi Query: Precision={multi_precision:.2f}, "
    f"Recall={multi_recall:.2f}"
)

def reciprocal_rank_fusion(results,k=60):
    rrf_scores={}
    document_store={}

    for result_list in results:
        for rank,doc in enumerate(result_list,start=1):
            #doc_id=doc.metadata.get("source")
            doc_id=doc.page_content
            #if not doc_id:
                #doc_id=doc.page_content

            if doc_id not in rrf_scores:
                rrf_scores[doc_id]=0
                document_store[doc_id]=doc
                rrf_scores[doc_id]+=1/(k+rank)

    ranked_document= sorted(
        rrf_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        (document_store[doc_id],score) for doc_id,score in ranked_document
    ]

fused_results = reciprocal_rank_fusion(
    retrieval_result
)


# Display results
print("\n===== RRF RERANKED RESULTS =====")

for index, (doc, score) in enumerate(
    fused_results[:5],
    start=1
):

    print(f"\nRank: {index}")
    print(f"Source: {doc.metadata.get('source')}")
    print(f"RRF Score: {score:.5f}")
    print(f"Content: {doc.page_content[:250]}")


# Compare retrieval approaches

print("\n===== TOP 5 RETRIEVAL COMPARISON =====")

single_results = vectorstore.similarity_search(
    question,
    k=5
)

print("\n--- SINGLE QUERY ---")

for i, doc in enumerate(single_results, 1):
    print(i, doc.metadata.get("source"))

print("\n--- MULTI-QUERY WITH DEDUPLICATION ---")

for i, doc in enumerate(unique_results.values(), 1):
    if i > 5:
        break
    print(i, doc.metadata.get("source"))

print("\n--- MULTI-QUERY WITH RRF ---")

for i, (doc, score) in enumerate(fused_results[:5], 1):
    print(i, doc.metadata.get("source"), round(score, 5))