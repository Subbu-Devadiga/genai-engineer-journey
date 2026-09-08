from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client=OpenAI()

text="I want to become an GenAI Engineer"

response=client.embeddings.create(
    model="text-embedding-3-small",
    input=text
)

embedding=response.data[0].embedding

print("Text :")
print(text)

print("\nNumber of dimensions :")
print(len(embedding))

print("\nFirst 10 values")
print(embedding[:10])