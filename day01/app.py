from openai import openAI

client=openAI()

response= client.responses.create(
    model="Your_model",
    input="Expalin RAG in simple steps"
)

print(response.output_text)