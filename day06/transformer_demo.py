from transformers import pipeline

classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

texts = [
    #"The change request was approved by the CAB.",
    #"The deployment caused a production outage.",
    #"The release was successfully completed.",
    "The application is working perfectly.",
    "The application is completely broken.",
    "The change implementation was successful.",
    "The change implementation failed."
]


for text in texts:
    result = classifier(text)

    print(f"\nText: {text}")
    print(f"Result: {result}")