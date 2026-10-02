import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
from documents import documents

load_dotenv()
client=OpenAI()

def get_embedding(text):
    response=client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding

def cosine_similarity(a,b):
    a=np.array(a)
    b=np.array(b)

    return np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))

document_embeddings=[]

for document in documents:
    embedding=get_embedding(document["text"])

    document_embeddings.append({
        "id": document["id"],
        "text": document["text"],
        "embedding": embedding
    })

query = "What should I verify before implementing a production change?"
query_embedding=get_embedding(query)

results=[]

for document in document_embeddings:
    score = cosine_similarity(
        query_embedding,
        document["embedding"]
    )
    results.append({
        "id":document["id"],
        "score": score,
        "text": document["text"]
    })


results.sort( key=lambda x: x["score"],
            reverse=True)

print("\nQuery:")
print(query)

print("\nTop results:")

for result in results[:3]:
    print(f"\n{result['id']}")
    print(f"Score: {result['score']:.4f}")
    print(result["text"].strip())