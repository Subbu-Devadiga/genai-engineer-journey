from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
model=ChatOpenAI(
    model="gpt-6-astra"
)

prompt=ChatPromptTemplate.from_template(
 """
    Explain this IT change management concept in one sentence:

    {concept}
    """
)

parser=StrOutputParser()

chain=prompt | model | parser

result=chain.invoke(
    {
        "concept": "Change Advisory Board"
    }
)

print(result)