from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client=OpenAI()

response=client.responses.create(
    model="gpt-6-astra",
    input='''
Example 1:Change: Update a UI color.
Risk: Low

Example 2:
Change: Modify production database schema.
Risk: High

Now classify:
Change: Restart production application servers. '''
)
print(response.output_text)