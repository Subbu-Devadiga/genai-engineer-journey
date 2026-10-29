import re

def word_overlap_score(answer : str, context : str) -> float:
    """A simple lexical-overlap metric for learning purposes."""
    stop_words={
        "a", "an", "the", "is", "are", "was", "were",
        "and", "or", "if", "to", "of", "in", "on",
        "for", "it", "this", "that", "how", "what",
        "with", "be", "as", "by"
    }

    def meaningful_words(text):
        return {
            word for word in re.findall(r"\b[a-z]+\b", text.lower())
            if word not in stop_words
        }

    answer_words=meaningful_words(answer)
    context_words=meaningful_words(context)

    if not answer_words or not context_words:
        return 0.0

    return len(answer_words & context_words)/len(answer_words)

test_cases=[
    {
        "name": "Rollback plan",
        "question": "What is a rollback plan?",
        "context": (
            "A rollback plan explains how to restore the previous "
            "working state if a change fails."
        ),
        "answer": (
            "A rollback plan explains how to restore the previous "
            "working state if a change fails."
        ),
        "answerable": True,
    },
    {
        "name": "Emergency change",
        "question": "What documentation is required for an emergency change?",
        "context": (
            "Emergency changes require documented justification, "
            "risk and impact assessment, implementation and rollback "
            "plans, appropriate emergency authorization, and "
            "retrospective review."
        ),
        "answer": (
            "Emergency changes require documented justification, "
            "risk and impact assessment, implementation and rollback "
            "plans, emergency authorization, and retrospective review."
        ),
        "answerable": True,
    },
    {
        "name": "Unknown CAB limit",
        "question": "What is the maximum number of CAB members?",
        "context": (
            "CAB reviews proposed changes, risks, impacts, and "
            "required approvals."
        ),
        "answer": (
            "The maximum number of CAB members is 12."
        ),
        "answerable": False,
    },
    {
        "name": "Misleading rollback answer",
        "question": "What is a rollback plan?",
        "context": (
            "A rollback plan explains how to restore the previous "
            "working state if a change fails."
        ),
        "answer": (
            "A rollback plan requires 12 CAB members."
        ),
        "answerable": False,
    },
]

def evaluate():
    total=len(test_cases)
    correct=0

    print("=== Day 22: RAG Evaluation ===\n")

    for case in test_cases:
        score=word_overlap_score(case["answer"], case["context"])

        predicted_supported=score>0.60

        expected_supported=case["answerable"]

        passed=predicted_supported==expected_supported

        correct+=int(passed)


        print(f"Test :{case["name"]}")
        print(f"Question : {case["question"]}")
        print(f"Overlap score : {score:.2f}")
        print(f"Predicted supported : {predicted_supported}")
        print(f"Expected supported : {expected_supported}")
        print(f"Test result : {'PASS' if passed else 'FAIL'}")
        print("-" *45)

    print(f"\nDecision accuracy: {correct}/{total} "
          f"({correct / total:.0%})")


if __name__=="__main__":
    evaluate()
