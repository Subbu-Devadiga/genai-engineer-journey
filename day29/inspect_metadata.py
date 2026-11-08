import os
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma


load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OpenAI key not found")

embeddings=OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vectorstore=Chroma(
    collection_name="Change_management",
    embedding_function=embeddings,
    persist_directory="../day08/chroma_db"
)

data=vectorstore.get()

print("-----------Available metadata ------------")

for index,metadata in enumerate(data["metadatas"][:10],start=1):
    print(f"\nDocument {index} :")
    print(metadata)