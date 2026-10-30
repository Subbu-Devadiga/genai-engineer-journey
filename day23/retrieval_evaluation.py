from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

embeddings=OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vectorstore=Chroma(
    collection_name="Change_management",
    embedding_function=embeddings,
    persist_directory="../day08/chroma_db"
)

k=5

test_cases=[
    {

        "question": "What is a rollback plan?",
        "expected_sources": {"rollback"}
    },
    {
        "question": "What documentation is required for an emergency change?",
        "expected_sources": {"emergency_change"}
    },
    {
        "question": "What should I validate before implementing a production change?",
        "expected_sources": {"production_validation",
    "staging_and_uat",
    "normal_change"}
    }
    
    
]

def evaluate_retrieval(question,expected_sources):
    result=vectorstore.similarity_search_with_score(question, k=k)

    retrieved_sources=[doc.metadata.get("source", "unknown") for doc,score in result]

    relevant_retrieved=set(retrieved_sources) & expected_sources

    precision=len(relevant_retrieved)/k

    recall=len(relevant_retrieved)/len(expected_sources) if expected_sources else 0

    print(f"\nQuestion: {question}")
    print(f"Expected sources: {expected_sources}")
    print(f"Retrieved sources: {retrieved_sources}")
    print(f"Relevant retrieved: {relevant_retrieved}")
    print(f"Precision@{k}: {precision:.2f}")
    print(f"Recall@{k}: {recall:.2f}")

if __name__=="__main__":
    for test in test_cases:
        evaluate_retrieval(test["question"],test["expected_sources"])

        

