from openai import OpenAI
from dotenv import load_dotenv
import chromadb


load_dotenv()
openai_client=OpenAI()

chroma_client=chromadb.PersistentClient(
    path="../day08/chroma_db"
)

collection=chroma_client.get_or_create_collection(
    name="Change_management"
)

def get_embedding(text):
    response=openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding

def retrieve_documents(query,top_k=5,environment=None):
    query_embedding=get_embedding(query)
    where_filter=None

    if environment:
        where_filter={"environment":environment}

    results=collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where=where_filter    )

    documents=results["documents"][0]
    ids=results["ids"][0]
    distances=results["distances"][0]

    return documents,ids,distances


def generate_answer(question,documents):
    context="\n\n".join(documents)
    instructions="""
You are an enterprise IT Change Management Assistant.

Answer the user's question using only the provided context.

Rules:
1. Do not invent information.
2. If the answer is not available in the context, say:
   "The provided knowledge base does not contain enough information."
3. Give a concise and practical answer.
"""

    prompt=f"""
    Context: {context}
    question : {question}
    """
    response=openai_client.responses.create(
        model="gpt-6-astra",
        instructions=instructions,
        input=prompt
    )

    return response.output_text

while True:
    question=input("Enter your question (or type 'exit' to quit):")

    if question.lower()=="exit":
        break

    documents, ids, distances=retrieve_documents(question,top_k=5)

    print("\n Retrieved documents:")
    for i,document_id in enumerate(ids):
        print(
            f"{i + 1}. {document_id} "
            f"| distance: {distances[i]:.4f}"
        )

    answer=generate_answer(question,documents)

    print("\n==============================")
    print("RAG ANSWER")
    print("==============================")

    print(answer)
