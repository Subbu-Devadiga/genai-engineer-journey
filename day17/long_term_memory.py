from langgraph.store.memory import InMemoryStore

store=InMemoryStore()

# A namespace separates this user's memory from other users.
namespace=("change_management","user_001")
user2_namespace=("change_management","user002")
# 1. Save selected facts
store.put(
    namespace,
    "environment_preference",
    {
        "preferred_environment": "UAT",
        "application": "Customer Payment Service",
    },
)

store.put(
    namespace,
    "response_preference",
    {
        "response_style" : "Step-by-step explanations",
    },
)

store.put(
    namespace,
    "answer_format",
    {
        "format": "Numbered steps",
        "detail_level": "Detailed",
    },
)

print("\n------------Memory Saved-----------")

environment_memory=store.get(
    namespace,
    "environment_preference",
)

if environment_memory:
    print("\nEnvironment memory:")
    print(environment_memory.value)

# 3. Retrieve all memories in this namespace
print("\n--- All memories for this user ---")

for item in store.search(namespace):
    print(f"Memory ID : {item.key}")
    print(f"Memory value : {item.value}")
    print()


# 4. Simulate a separate conversation using the same user namespace.
# The facts can be retrieved without replaying the original conversation.
print("--- New conversation: retrieving useful context ---")

saved_preference = store.get(
    namespace,
    "environment_preference",
)

if saved_preference:
    environment = saved_preference.value["preferred_environment"]
    application = saved_preference.value["application"]

    print(f"Relevant environment: {environment}")
    print(f"Relevant application: {application}")

print("\n--- Retrieve answer format only ---")

format_memory = store.get(
    namespace,
    "answer_format",
)

if format_memory:
    print(format_memory.value)
else:
    print("No answer-format preference found.")


print("\n--- User 2 memory isolation test ---")

user2_memory = store.get(
    user2_namespace,
    "environment_preference",
)

if user2_memory:
    print(user2_memory.value)
else:
    print("No environment preference found for User 2.")