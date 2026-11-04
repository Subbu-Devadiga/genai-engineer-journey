from datasets import Dataset

question=[
    "What is a rollback plan?",
    "How do I recover after a deployment failure?",
    "What should be considered before implementing a production change?"
]

contexts=[
    [
        "A rollback plan describes how to restore the previous stable state if a change fails."
    ],
    [
        "Rollback procedures help restore the previous stable state after deployment failure.",
        "Recovery procedures may involve workarounds, restarts, traffic redirection and rollback."
    ],
    [
        "Production changes should be reviewed for risk, impact, implementation steps, validation activities and rollback procedures."
    ]
]

answers=[
    "A rollback plan describes how to restore the previous stable state if a change fails.",
    "After a deployment failure, follow the documented recovery procedure. This may involve restarting services or executing the rollback procedure to restore the previous stable state.",
    "Before implementing a production change, review its risk, impact, implementation steps, validation activities and rollback procedures."
]

ground_truths=[
     "A rollback plan explains how to restore the previous stable state if a change fails.",
    "Follow the recovery procedure, which may involve workarounds, restarts, traffic redirection or rollback.",
    "Review risk, impact, implementation steps, validation activities and rollback procedures."
]

data={
    "question" : question,
    "contexts" : contexts,
    "answer" : answers,
    "ground_truth" : ground_truths
}

dataset=Dataset.from_dict(data)

if __name__ == "__main__":
    print("===== RAG EVALUATION DATASET =====")
    print(dataset)

    for index,item in enumerate(dataset,1):
        print(f"\nTest Case: {index}")
        print("Question:", item["question"])
        print("Answer:", item["answer"])
        print("Context:", item["contexts"])
        print("Ground Truth:", item["ground_truth"])