
import re
from rank_bm25 import BM25Okapi

# Sample enterprise change-management documents
documents = [
    {
        "source": "rollback",
        "content": """
        A rollback plan describes how to restore the previous
        stable state if a change fails.
        """
    },
    {
        "source": "emergency_change",
        "content": """
        Emergency changes address critical incidents and
        require appropriate emergency authorization.
        """
    },
    {
        "source": "production_validation",
        "content": """
        Production changes require validation activities,
        functional testing, monitoring and log verification.
        """
    },
    {
        "source": "change_request",
        "content": """
        Change requests must include a unique change identifier,
        such as CHG0012345, along with risk and impact details.
        """
    },
    {
        "source": "incident_management",
        "content": """
        Incident management focuses on restoring normal
        service operations after an interruption.
        """
    }
]


# Tokenization
def tokenize(text):
    return re.findall(r"[a-z0-9]+", text.lower())


# Prepare tokenized documents
tokenized_documents = [
    tokenize(doc["content"])
    for doc in documents
]

# Build BM25 index
bm25 = BM25Okapi(tokenized_documents)


# Search function
def bm25_search(query, top_k=3):

    query_tokens = tokenize(query)

    scores = bm25.get_scores(query_tokens)

    ranked_indices = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )

    print(f"\nQuestion: {query}")
    print("-" * 50)

    for index in ranked_indices[:top_k]:
        print("Source:", documents[index]["source"])
        print("BM25 Score:", round(float(scores[index]), 4))
        print("Content:", documents[index]["content"].strip())
        print("-" * 50)


if __name__ == "__main__":

    bm25_search("What is a rollback plan?")

    bm25_search("CHG0012345")

    bm25_search("production validation and testing")
