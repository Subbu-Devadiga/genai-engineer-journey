\# Day 07 - LLM Engineering



\## Topics



\- LLM inference

\- Prompt engineering

\- Zero-shot prompting

\- Few-shot prompting

\- Instructions and user input

\- Structured outputs

\- JSON vs Structured Outputs

\- Pydantic



\## Practical Work



\- Called an LLM using the Responses API

\- Built prompts for change-management analysis

\- Compared zero-shot and few-shot prompting

\- Generated structured change-analysis data

\- Parsed structured output using Pydantic



\## Key Takeaway



An LLM becomes useful in production when it is integrated

with application logic, structured outputs, validation,

data and business workflows.









What is LLM inference?

LLM inference is using a pre-trained model to produce output for new input.



What is prompt engineering?

Prompt engineering is the instruction/context you provide to the model. A quality prompting usually gives model a role/task, constraints, context and desired output. 



What is zero-shot prompting?

Zero shot prompting is giving the model a task without any example.



What is few-shot prompting?

Few shot prompting is to give model a few examples before providing an actual task.



What is the difference between instructions and user input?

User input is the text or requirement given by user that tells what information user need. While instruction is something that tells the model what role it should perform to produce the requested result. For example "Act as a finance advisor".



Why is structured output useful in an LLM application?

Structured outputs can be efficiently stored in database and python applications can efficiently process the structured output.



What is the difference between JSON mode and Structured Outputs?

Json mode doesn't mean it to be necessarily in specific schema. In structured outputs we can define the schema and outputs will follow that schema



Why shouldn't an application blindly trust free-form LLM output?

Trusting free-form LLM application may introduce severe security vulnerabilities, data integrity issues and system instability.



What is Pydantic and why can it be useful with LLM applications?

Pydantic is a python library used for data validation and supports defining a schema



Explain the flow:



User Input

&#x20;  ↓

Prompt / Instructions

&#x20;  ↓

LLM

&#x20;  ↓

Structured Output

&#x20;  ↓

Python Application



User input is the raw text given by the user and prompts gives the model what role/context the model should perform. Then user input and prompts will be passed to LLM model by calling an APIs. LLM evaluates context, extract relevant variables and produces structured output with the relevant schema so that the python applications can use it.





What is the difference between training an LLM and inference?

Training a model is optimizing model parameter using data. Training from scratch starts with randomly initialized parameters and requires large amount of data. Inference is using a pre-trained model, where model is already undergone training and learned useful patterns. So we can use it directlu to produce output for new data



Why is structured output particularly useful in enterprise applications?

Unstructured output is difficult to store in database and it is not efficient way if it needs to be used by some python application. While structured outputs can be stored efficiently in database and we can define schema to structured outputs so that enterprise applications can use it efficiently.



Suppose an LLM returns:



{

&#x20;   "risk": "High",

&#x20;   "rollback": true

}



Why is this more useful to a Python application than:



"This looks like a high-risk change and fortunately

there is a rollback plan."



It is an structured output and it is in Json format where python applications can process it easily.





What would happen if an LLM application accepted arbitrary free-form output and directly used it to trigger an important business action?

It may lead to severe security vulnerabilities, data integrity issues and system instability.

