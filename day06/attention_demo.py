from transformers import AutoTokenizer

tokenizer=AutoTokenizer.from_pretrained("distilbert-base-uncased")

#text="I want to become a GENAI engineer"
#text = "Generative AI is transforming software engineering."
text = "I am learning GenAI engineering."

tokens=tokenizer.tokenize(text)
token_ids=tokenizer.encode(text)

print("Original text:")
print(text)

print("\nTokens:")
print(tokens)

print("\nToken IDs:")
print(token_ids)