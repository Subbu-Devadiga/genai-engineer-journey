from dotenv import load_dotenv
from operator import itemgetter

from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI,OpenAIEmbeddings

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (RunnablePassthrough, RunnableParallel,RunnableLambda)

load_dotenv()

#embedding model
embeddings=OpenAIEmbeddings(
    model="text-embedding-3-small"
)

#Connect to existing chromadb
vectorstore=Chroma(
    collection_name="Change_management",
    embedding_function=embeddings,
    persist_directory="../day08/chroma_db"
)

#Convert vector store into retriever
retriever=vectorstore.as_retriever(
    search_kwargs={"k": 3}
)


#LLM
model=ChatOpenAI(
    model="gpt-6-astra"
)

#prompt
prompt=ChatPromptTemplate.from_template(
    """
    You are an enterprise IT Change Management assistant.

    Answer the question using ONLY the provided context.

    If the answer is not available in the context, say:
    "The provided knowledge base does not contain enough information."

    Context:
    {context}

    Question:
    {question}
    """
)


# 6. Convert retrieved documents into plain text
def format_docs(docs):
    return "\n\n".join(
        doc.page_content for doc in docs
        )
#extract source ids
def format_sources(docs):
    return "\n\n".join(
        f"- {doc.metadata.get('source',doc.metadata.get('id','unknown'))}" for doc in docs
    )

# Convert Python functions into LangChain Runnables
format_docs_runnable = RunnableLambda(format_docs)
format_sources_runnable = RunnableLambda(format_sources)

#Retrieve docuents and keep the original question
retrieval=RunnableParallel(
    docs=retriever,
    question=RunnablePassthrough()
)
# generate answer 
answer_chain = (
    {
        "context": lambda x: format_docs(x["docs"]),
        "question": lambda x: x["question"]
    }
    | prompt
    | model
    | StrOutputParser()
)

#Return both answer and sources
rag_chain=( retrieval | RunnableParallel(
    answer=answer_chain,
    sources=lambda x: format_sources(x["docs"])
)
)

# 8. Ask a question
question = input("Enter your question: ")

result = rag_chain.invoke(question)

print("\nAnswer:")
print(result['answer'])

print("\nSources:")
print(result["sources"])