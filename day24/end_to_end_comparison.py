from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI,OpenAIEmbeddings

load_dotenv()

embeddings=OpenAIEmbeddings(model="text-embedding-3-small")

vectorstore=Chroma(
    collection_name="Change_management",
    embedding_function=embeddings,
    persist_directory="../day08/chroma_db"
)

llm=ChatOpenAI(model="gpt-6-astra")

test_cases=[
    {
        "question": "What is a rollback plan?",
        "expected_sources": {"rollback"}
    },
    {
        "question": "What documentation is required for an emergency change?",
        "expected_sources": {"emergency_change"}
    },
    {
        "question": "What should I validate before implementing a production change?",
        "expected_sources": {
            "production_validation",
            "staging_and_uat",
            "normal_change"
        }
    }
]

def evaluate_retrieval(docs,expected_sources):
    retrieved={
        doc.metadata.get("source","unknown") for doc in docs
    }

    relevant=retrieved.intersection(expected_sources)

    precision=(len(relevant)/len(retrieved)
               if retrieved else 0
               )

    recall=(len(relevant)/len(expected_sources)
            if expected_sources else 0
            )

    return retrieved,precision,recall

def generate_answer(question,docs):
    context="\n\n".join(
            f"Source : {doc.metadata.get("source","unnown")}\n"
            f"Content : {doc.page_content}"
            for doc in docs
        )

    prompt=f"""
You are an enterprise Change Management assistant.

Answer the question using ONLY the provided context.

Rules:
1. Do not invent enterprise policies.
2. Do not use outside knowledge.
3. Cite supporting source IDs in your answer.
4. If the context does not contain sufficient information,
   respond: Insufficient information.

Context:
{context}

Question:
{question}

Answer:
"""

    response=llm.invoke(prompt)
    return response.content

K=3


strategies=["Similarity","mmr"]

for case in test_cases:
    question=case["question"]
    expected=case["expected_sources"]

    print("\n" + "=" * 65)
    print("QUESTION:", question)
    print("EXPECTED SOURCES:", expected)

    for strategy in strategies:
        if strategy=="Similarity":
            docs=vectorstore.similarity_search(
                question,
                k=K
            )
            retrieved,precision,recall=evaluate_retrieval(
                                    docs,expected
                                )
            answer = generate_answer(question, docs)
            
            print("\n---", strategy.upper(), "---")
            print("Retrieved sources:", retrieved)
            print(f"Precision@{K}: {precision:.2f}")
            print(f"Recall@{K}: {recall:.2f}")
            print("Generated answer:")
            print(answer)
        else:
            mmr_configs = [
                        {"fetch_k": 5, "lambda_mult": 0.0},
                        {"fetch_k": 5, "lambda_mult": 0.5},
                        {"fetch_k": 5, "lambda_mult": 1.0},
                        {"fetch_k": 10, "lambda_mult": 0.0},
                        {"fetch_k": 10, "lambda_mult": 0.5},
                        {"fetch_k": 10, "lambda_mult": 1.0},
                        {"fetch_k": 15, "lambda_mult": 0.0},
                        {"fetch_k": 15, "lambda_mult": 0.5},
                        {"fetch_k": 15, "lambda_mult": 1.0}
                        ]

            
            for config in mmr_configs:

                docs = vectorstore.max_marginal_relevance_search(
            question,
            k=K,
            fetch_k=config["fetch_k"],
            lambda_mult=config["lambda_mult"]
            )
                

                retrieved,precision,recall=evaluate_retrieval(
                                                docs,expected
                                            )
                answer = generate_answer(question, docs)

                print("\n---", strategy.upper(), "---")
                print("\nConfiguration:", config)
                print("Retrieved sources:", retrieved)
                print(f"Precision@{K}: {precision:.2f}")
                print(f"Recall@{K}: {recall:.2f}")
                print("Generated answer:")
                print(answer)
        





    
