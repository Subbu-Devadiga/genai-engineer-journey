import chromadb
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client=OpenAI()

chroma_client=chromadb.PersistentClient(
    path="../day08/chroma_db"
)

collection=chroma_client.get_or_create_collection(
    name="Change_management"
)

def get_embedding(text):
    response=client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding

def retrieve_documents(query,top_k=3):
    query_embedding=get_embedding(query)

    results=collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents","distances"]
    )
    documents=results["documents"][0]
    ids=results["ids"][0]
    distances=results["distances"][0]
    return  documents,ids,distances

def generate_answer(question,documents):
    context="\n\n".join(documents)
    instruction="""
You are an enterprise IT Change Management Assistant.

Answer the user's question using only the provided context.

Rules:
1. Do not invent information.
2. If the answer is not available in the context, say:
   "The provided knowledge base does not contain enough information."
3. Give a concise and practical answer.
"""

    prompt=f"""
Context:
{context}

user question:
{question}
"""

    response=client.responses.create(
        model="gpt-6-astra",
        instructions=instruction,
        input=prompt
    )

    return response.output_text

while True:
    question = input("\nEnter your question (or type 'exit'): ")

    if question.lower() == "exit":
        break

    documents,source_ids,distances=retrieve_documents(question)

    print("\n Retrieved context:")
    for i,doc in enumerate(documents):
        print(f"\n---Document {i+1}---:")
        print(doc)

    answer=generate_answer(question,documents)

    print("\n==============================")
    print("RAG ANSWER")
    print("==============================")
    print(answer)

    print("\nSources:")
    for source_id in source_ids:
        print(f"- {source_id}")

    print("\nRetrieved Sources:")

    for source_id, distance in zip(source_ids, distances):
        print(
        f"- {source_id} | distance: {distance:.4f}"
    )
