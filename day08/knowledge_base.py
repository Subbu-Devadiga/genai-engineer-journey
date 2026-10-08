import chromadb
from openai import OpenAI
from dotenv import load_dotenv
from documents import documents
load_dotenv()
client=OpenAI()

chroma_client=chromadb.PersistentClient(
    path="./chroma_db"
)

collection=chroma_client.get_or_create_collection(
    name="Change_management"
)

for document in documents:
    response=client.embeddings.create(
        model="text-embedding-3-small",
        input=document["text"]
    )
    embedding=response.data[0].embedding
    collection.upsert(
        ids=[document["id"]],
        documents=[document["text"]],
        embeddings=[embedding],
        metadatas=[{
        "category": document["category"],
        "type": document["type"],
        "source": document["id"]
        }]
    )

print("Documents stored:",collection.count())

#query="What should I verify before implementing a production change?"
#query="What is an emergency change?"
#query="How should a failed production deployment be recovered?"
#query="What should happen after a successful change implementation?"
query="What is the difference between incident management and change management?"

query_response=client.embeddings.create(
    model="text-embedding-3-small",
    input=query
)

query_embedding=query_response.data[0].embedding

results=collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

print("\nQuery:")
print(query)

print("\nRetrieved documents:")

for i, document in enumerate(results["documents"][0]):
    print(f"\nResult {i + 1}:")
    print(document)