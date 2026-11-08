import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv("../.env")

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found")

llm=ChatOpenAI(
    model="gpt-6-astra"
)

prompt=ChatPromptTemplate.from_template(
    """
You are an intelligent query router for an
Enterprise Change Management knowledge assistant.

Classify the user's question into exactly one category:

1. VECTOR_SEARCH:
   For conceptual questions requiring semantic document retrieval.

2. METADATA_FILTER:
   For questions requesting specific records using
   attributes such as change type, application or environment.

3. MULTI_QUERY:
   For complex questions requiring multiple related
   searches to retrieve comprehensive information.

Return only the category name.

User question: {question}
"""
)

router=prompt | llm | StrOutputParser()

test_questions=[
    "What is the rollback procedure?",
    "Find emergency changes related to SAP in production.",
    "How do I recover after a failed production deployment?"
]

for question in test_questions:
    route=router.invoke(
        {"question" : question}
    )

    print("\n question : ",question)
    print("selected rute : ",route.strip())
