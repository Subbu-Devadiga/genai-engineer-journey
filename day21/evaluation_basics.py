
import re

def validate_answer(answer: str, supporting_context: str) -> bool:
    if not answer.strip() or not supporting_context.strip():
        return False

    # Normalize text and extract meaningful words.
    stop_words = {
        "a", "an", "the", "is", "are", "was", "were",
        "and", "or", "if", "to", "of", "in", "on",
        "for", "it", "this", "that", "how", "what",
        "with", "be", "as", "by"
    }

    answer_words = {
        word for word in re.findall(r"\b[a-z]+\b", answer.lower())
        if word not in stop_words
    }

    context_words = {
        word for word in re.findall(r"\b[a-z]+\b", supporting_context.lower())
        if word not in stop_words
    }

    if not answer_words:
        return False

    overlap = answer_words & context_words
    overlap_ratio = len(overlap) / len(answer_words)

    return overlap_ratio >= 0.6


def route_request(risk : str, validation_passed : bool) ->str:
    """Choose a safe next step based on validation and risk."""
    if not validation_passed:
        return "Insufficient_information"

    if risk.lower()=="high":
        return "human_review"

    return "approved_for_response"

def run_tests():
    tests=[
        {
            "name": "Supported answer",
            "answer": "A rollback plan restores the previous working state.",
            "context": "A rollback plan restores the previous working state.",
            "expected": True,
        },
        {
            "name": "Missing context",
            "answer": "The maximum number of CAB members is 12.",
            "context": "",
            "expected": False,
        },
        {
            "name": "Empty answer",
            "answer": "",
            "context": "A rollback plan restores the previous working state.",
            "expected": False,
        },
        {
            "name": "Unsupported answer with context present",
            "answer": "A rollback plan requires 12 CAB members.",
            "context": "A rollback plan explains how to restore the previous working state.",
            "expected": False,
        },
    ]

    passed=0

    for test in tests:
        actual=validate_answer(test["answer"],test["context"])
        success=actual==test["expected"]

        print(f"{test["name"]} : {'PASS' if success else 'FAIL'} ")
        passed+=int(success)

    print(f"\nResult : {passed}/{len(tests)} tests passed")

    print("Routing tests : ")
    print(route_request("normal", True))   # approved_for_response
    print(route_request("normal", False))  # insufficient_information
    print(route_request("high", True))     # human_review

if __name__=="__main__":
    run_tests()