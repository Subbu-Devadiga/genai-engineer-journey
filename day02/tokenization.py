import tiktoken

encoding=tiktoken.get_encoding("cl100k_base")
text="I want to become a GenAI Engineer"
tokens=encoding.encode(text)

print("Original text :")
print(text)


print("\nToken IDs : ")
print(tokens)

print("\n Number of tokens")
print(len(tokens))

print("\n Decoded tokens : ")
for token in tokens:
    print(token,"-->",encoding.decode([token]))
