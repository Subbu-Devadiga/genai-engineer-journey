from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client=OpenAI()
change_request = """
The application logo will be updated on the internal
employee portal. No backend services will be modified.
"""
response=client.responses.create(
    model="gpt-6-astra",
    instructions="""
You are an IT Change Management Assistant.

Analyze the change request provided by the user.

Identify:
1. Change type
2. Risk
3. Business impact
3. Rollback plan
4. Validation steps

Keep the response concise.
""",
    input=change_request
)

print(response.output_text)