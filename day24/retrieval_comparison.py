from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

embeddings=OpenAIEmbeddings(model="text-embedding-3-small")

vectorstore=Chroma(
    collection_name="Change_management",
    embedding_function=embeddings,
    persist_directory="../day08/chroma_db"
)

question=(
    "What should I consider before implementing "
    "a production change?"
)

k=3
print("\n===== SIMILARITY SEARCH =====")

similarity_results=vectorstore.similarity_search(
    question,
    k=k
)

for index,doc in enumerate(similarity_results,1):
    print(f"\nDocument {index}")
    print("Source :",doc.metadata.get("source"))
    print("Content :", doc.page_content[:250])

print("\n===== MMR SEARCH =====")

mmr_search=vectorstore.max_marginal_relevance_search(
    question,
    k=k,
    fetch_k=10,
    lambda_mult=0.2
)

for index,doc in enumerate(mmr_search,1):
    print(f"\nDocument {index}")
    print("Source :", doc.metadata.get("source"))
    print("Content",doc.page_content[:250])
    