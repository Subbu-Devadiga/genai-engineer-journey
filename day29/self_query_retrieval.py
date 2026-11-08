import os
import json

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma

load_dotenv("../.env")

llm=ChatOpenAI(
    model="gpt-6-astra",
    temperature=1
)

embeddings=OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vectorstore=Chroma(
    collection_name="Change_management",
    embedding_function=embeddings,
    persist_directory="../day08/chroma_db"
)

prompt=ChatPromptTemplate.from_template(
    """
You are a metadata extraction assistant.

Available metadata fields:
- category: Change Management, Release Management
- type: Procedure
- source: normal_change, emergency_change, cab, rollback,
  production_validation, change_closure, release_planning,
  build and packaging, deployment_strategy, staging_and_uat

Extract the metadata filters from the user question.

Return valid JSON in this format:
{{
    "filter": {{
        "category": "Change Management"
    }}
}}

If no metadata filter is needed, return:
{{"filter": null}}

User question: {question}
"""
)

chain=prompt | llm
question = "Find all Release Management procedures"
response=chain.invoke(
    {"question" : question}
)

print("------------Extracted metadata filters-------------")
result=json.loads(response.content)
metadata_filter=result["filter"]

if metadata_filter and len(metadata_filter)>1:
    metadata_filter={
        "$and" : [
            {key : value}
            for key,value in metadata_filter.items()
        ]
    }
print(metadata_filter)

if metadata_filter:
    documents=vectorstore.similarity_search(
        question,
        k=5,
        filter=metadata_filter
    )

else:
    documents=vectorstore.similarity_search(
        question,
        k=5
    )

print("------------Filtered retrieval results ------------")
for index,doc in enumerate(documents,start=1):
    print(f"\nDocument {index} :")
    print("Source : ",doc.metadata.get("source"))
    print("Category : ",doc.metadata.get("category"))
    print("Type : ",doc.metadata.get("type"))
    print("Content : ",doc.page_content[:250])