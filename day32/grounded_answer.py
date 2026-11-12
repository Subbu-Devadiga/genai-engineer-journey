import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_chroma import Chroma

from langchain_core.documents import Document
load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("Open AI key not found")

embeddings=OpenAIEmbeddings(
    model="text-embedding-3-small"
)

llm=ChatOpenAI(
    model="gpt-6-astra",
    temperature=1
)

vectorstore=Chroma(
    collection_name="Change_management",
    embedding_function=embeddings,
    persist_directory="../day08/chroma_db"
)

grounded_prompt=ChatPromptTemplate.from_template("""
You are an Enterprise Change Management assistant.

Answer the user's question using ONLY the provided context.

STRICT RULES:
1. Do not use external or pretrained knowledge.
2. Do not invent missing procedures or information.
3. Cite the source document for every factual claim.
4. Use citations in this format: [Source: document_name]
5. If the context is insufficient, clearly state:
   "I don't have sufficient information in the knowledge base
   to answer this question reliably."

Question:
{question}

Retrieved Context:
{context}

Generate a grounded answer:
""")

grounded_chain=grounded_prompt | llm | StrOutputParser()

print("grounded answer chain created successfuly..")

def format_context(documents):
    formatted_context=[]

    for index, doc in enumerate(documents,start=1):
        source=doc.metadata.get("source","unknown")
        formatted_context.append(f"""
        document {index}
        source : {source}
        content : {doc.page_content}
        """)

    return "\n".join(formatted_context)

print("grounded answer generation setup complete")

test_documents=[
    Document(
        page_content="A rollback plan restores the previous stable state.",
        metadata={"source": "rollback"}
    ),
    Document(
        page_content="Production changes require validation.",
        metadata={"source": "production_validation"}
    )
]

print(format_context(test_documents))

test_question= "What is the employee leave policy?"

retrieved_docs=vectorstore.similarity_search(
    test_question,
    k=5
)
test_context=format_context(retrieved_docs)

response=grounded_chain.invoke({
    "question" : test_question,
    "context": test_context
})

print("----------Grounded Answer--------")
print("Question :",test_question)
print("Answer :",response)