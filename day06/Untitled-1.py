


def total_messages(messages):
    total =len(messages)
    return total

def count_messages(messages):
    count_python=0
    count_genai=0
    for message in messages:
        if "python" in message.lower():
            count_python+=1
        if "genai" in message.lower():
            count_genai+=1

    return count_python,count_genai

def count_keyword(messages,keyword):
    count=0
    for message in messages:
        if keyword.lower() in message.lower():
            count+=1

    return count

def average_length(messages):
    message_count=len(messages)
    total_length=0
    for message in messages:
        total_length+=len(message)

    avg_length=total_length/message_count
    return avg_length

def longest(messages):
    length=0
    for message in messages:
        if len(message)>length:
            longest_message=message
            length=len(message)
        
    return longest_message

# def genAI_messages(messages):
#     count=0
#     for message in messages:
#         if "genai" in message.lower()
#         count+=1


messages = [
    "Hello, how are you?",
    "Python is interesting",
    "I want to learn GenAI",
    "Python is powerful",
    "I love programming",
    "Can you teach me Python?",
    "GENAI is changing software development"
]

def analyze_messages(messages):
    python_count,genAI_count=count_messages(messages)
    result_set={
    "total" : total_messages(messages),
    "Python messages": python_count,
    "Average length" : average_length(messages),
    "Logest message" : longest(messages),
    "GenAI count":genAI_count
    }
    return result_set

result= analyze_messages(messages)
print(result)
