import os
from dotenv import load_dotenv
from pydantic import BaseModel,Field
from typing import List

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv("../.env")

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("API key not found")

llm=ChatOpenAI(
    model="gpt-6-astra",
    temperature=1
)

class ClaimExtraction(BaseModel):
    claims : List[str] = Field(
        description="List of individual factual claims extracted from the answer."
    )

class ClaimVerification(BaseModel):
    claim:str = Field(
        description="Original factual claim"
    )

    status : str =Field(
        description="Must be SUPPORTED or UNSUPPORTED"
    )

    reason : str = Field(
        description="Explain why the context support or does not support the claim"
    )

class ClaimVerificationResults(BaseModel):
    results : List[ClaimVerification]=Field(
        description="Verification result for every extracted claim"
    )

structured_llm=llm.with_structured_output(ClaimExtraction)

claim_prompt=ChatPromptTemplate.from_template("""
You are an expert in factual claim extraction.

Extract every individual factual claim from the given answer.

Rules:
1. Each claim must represent one factual statement.
2. Do not combine multiple claims.
3. Do not add new information.
4. Ignore headings and formatting.
5. Preserve the original meaning.

Answer:
{answer}
""")

claim_chain=claim_prompt | structured_llm




verification_llm=llm.with_structured_output(ClaimVerificationResults)

verification_prompt=ChatPromptTemplate.from_template("""
You are a claim verification expert for an enterprise RAG system.

Evaluate each claim using ONLY the provided context.

Rules:
1. Mark SUPPORTED only when the context explicitly supports the claim.
2. Mark UNSUPPORTED if the context does not support the claim.
3. Do not use external or pretrained knowledge.
4. Evaluate every claim independently.
5. Provide a short reason for each decision.

Retrieved Context:
{context}

Claims:
{claims}
""")

verification_chain=verification_prompt | verification_llm



if __name__=="__main__":
    answer="""
    Application health checks, functional testing,
    monitoring and database backup restoration
    must be performed after production changes.
    """

    result=claim_chain.invoke({
        "answer": answer
    })

    print("\n------- Extracted claims ------------")

    for index,claim in enumerate(result.claims,start=1):
        print(f"{index}. {claim}")

    context="""
    Source: production_validation

    Production changes require application health checks,
    functional testing, monitoring and log verification.
    """
    Claims=[
    "Application health checks must be performed after production changes.",
    "Functional testing must be performed after production changes.",
    "Monitoring must be performed after production changes.",
    "Database backup restoration must be performed after production changes."
    ]

    result1=verification_chain.invoke(
        {
            "context" : context,
            "claims" : "\n".join(Claims)
        }
    )

    print("\n============== Claim verfifcation Result ====================")
    for item in result1.results:
        print("\nClaim : ",item.claim)
        print("Status : ",item.status)
        print("Reason : ",item.reason)