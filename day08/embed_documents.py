from openai import OpenAI
from dotenv import load_dotenv
from documents import documents

load_dotenv()
client=OpenAI()

for document in documents:
    response=client.embeddings.create(
        model="text-embedding-3-small",
        input=document["text"]
    )

    embedding=response.data[0].embedding

    print(f"ID: {document['id']}")
    print(f"Embedding dimensions: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")
    print()