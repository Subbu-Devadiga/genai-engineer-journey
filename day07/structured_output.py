from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
client=OpenAI()

class changeAnalysis(BaseModel):
    change_type:str
    risk_level: str
    rollback_available: bool
    validation_required: str

change_request = """
A production database schema will be modified tonight.
The change affects the customer transaction table.
A rollback script has been prepared.
The change is scheduled during the maintenance window.
"""
response=client.responses.parse(
    model="gpt-6-astra",
    instructions="""
You are an IT Change Management Assistant.

Analyze the change request and extract the required information.
Use the provided schema.
""",
input=change_request,
text_format=changeAnalysis
)

result=response.output_parsed

print("Change type:",result.change_type)
print("Risk level:",result.risk_level)
print("Rollback available:",result.rollback_available)
print("Validation required:",result.validation_required)
