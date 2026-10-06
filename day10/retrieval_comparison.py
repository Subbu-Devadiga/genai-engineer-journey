import chromadb
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

openai_client = OpenAI()

chroma_client = chromadb.PersistentClient(
    path="../day08/chroma_db"
)

collection = chroma_client.get_or_create_collection(
    name="Change_management"
)


def get_embedding(text):
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding


query = "What should I verify before implementing a production change?"

query_embedding = get_embedding(query)


for top_k in [1, 3, 5]:

    print("\n==============================")
    print(f"TOP-K = {top_k}")
    print("==============================")

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    ids = results["ids"][0]
    distances = results["distances"][0]

    for i, document_id in enumerate(ids):

        print(
            f"{i + 1}. {document_id} "
            f"| distance: {distances[i]:.4f}"
        )