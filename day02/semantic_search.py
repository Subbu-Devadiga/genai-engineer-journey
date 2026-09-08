from openai import OpenAI
from dotenv import load_dotenv
import numpy as np

load_dotenv()
client=OpenAI()

def get_embedding(text):
    response=client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding


def cosine_similarity(vector_a,vector_b):
    a=np.array(vector_a)
    b=np.array(vector_b)

    return np.dot(a,b)/(np.linalg.norm(a) * np.linalg.norm(b))


#query="How can I reset my password?"
query="How do I get access to my company VPN?"

'''
documents = [
    "How to change your corporate password",
    "Steps to reset your login credentials",
    "Today's weather forecast",
    "How to cook pasta"
]
'''
documents = [
    "How to connect to the corporate VPN",
    "Steps to reset your company password",
    "How to request laptop access",
    "How to prepare coffee"
]

query_embedding=get_embedding(query)

for document in documents:
    document_embedding=get_embedding(document)

    score=cosine_similarity(query_embedding,document_embedding)

    print(f"{score :.4f} --> {document}")
