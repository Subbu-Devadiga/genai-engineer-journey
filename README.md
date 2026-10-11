\# GenAI Engineer Journey —  of Hands-On Learning



A structured, hands-on journey toward becoming a Generative AI Engineer through practical coding, experimentation, and real-world projects.



This repository documents my progress in Python for AI engineering, machine learning, deep learning, Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), LangChain, LangGraph, and agentic AI workflows.



\*\*Goal:\*\* Build practical GenAI engineering skills and develop portfolio projects that demonstrate my ability to design, implement, and evaluate AI-powered applications.



\## About This Journey



I am building on my existing Python, SQL, and application development knowledge to develop practical GenAI engineering skills. My focus is on understanding the fundamentals, writing working code, solving implementation problems, and building applications relevant to enterprise environments.



The journey follows a hands-on approach, with daily exercises, code examples, documentation, interview preparation, and Git version control.



\## Learning Progress



| Days 	 | Topics  | Status |

| Day 01 | LLM fundamentals and first OpenAI API application | Completed |

| Day 02 | Tokenization, embeddings, and semantic similarity | Completed |

| Day 03 | Machine learning fundamentals and linear regression | Completed |

| Day 04 | Neural networks, activation functions, and backpropagation | Completed |

| Day 05 | PyTorch, tensors, autograd, and model training | Completed |

| Day 06 | Transformers and Hugging Face models | Completed |

| Day 07 | Prompt engineering and structured LLM outputs | Completed |

| Day 08 | Embeddings, vector databases, and ChromaDB | Completed |

| Day 09 | Building an end-to-end RAG application | Completed |

| Day 10 | Chunking, metadata, retrieval optimization, and reranking concepts | Completed |

| Day 11 | LangChain, LCEL, and source-aware RAG | Completed |

| Day 12 | LangGraph, conditional routing, and LLM-powered workflows | Completed |

| Day 13–50 | Advanced GenAI engineering, agents, evaluation, deployment, and portfolio projects | Planned |



\## Projects Built So Far



\### 1. LLM Applications

\- Integrated Python applications with the OpenAI API.

\- Practiced prompt engineering and structured output generation.

\- Used Pydantic to define expected response schemas.



\### 2. Machine Learning and Deep Learning Fundamentals

\- Implemented linear regression and gradient descent.

\- Built a simple neural network.

\- Practiced PyTorch tensors, autograd, loss functions, and optimization.



\### 3. Semantic Search and Vector Databases

\- Generated text embeddings using `text-embedding-3-small`.

\- Implemented cosine similarity and semantic search.

\- Created a persistent ChromaDB knowledge base with document metadata.



\### 4. Retrieval-Augmented Generation (RAG)

\- Built an end-to-end RAG application using an LLM and ChromaDB.

\- Implemented document retrieval and context-grounded responses.

\- Added source identification and basic abstention when the knowledge base lacks sufficient information.

\- Explored chunking, top-k retrieval, metadata filtering, hybrid search, and reranking concepts.



\### 5. LangChain RAG

\- Used prompt templates and LangChain Expression Language (LCEL).

\- Composed models, retrievers, and output parsers.

\- Built a source-aware RAG chain using `RunnableParallel` and other runnable components.



\### 6. LangGraph Change Management Workflow

\- Built stateful graphs using `StateGraph`.

\- Implemented nodes, edges, and conditional routing.

\- Integrated an LLM with structured Pydantic output.

\- Developed a preliminary change-risk assessment workflow that routes high-risk changes to enhanced review.



\## Technology Stack



\- \*\*Programming:\*\* Python

\- \*\*Machine Learning:\*\* NumPy, Pandas, PyTorch

\- \*\*LLMs and APIs:\*\* OpenAI API

\- \*\*LLM Frameworks:\*\* LangChain, LangGraph

\- \*\*Embeddings and Vector Search:\*\* OpenAI embeddings, ChromaDB

\- \*\*Model Integration:\*\* Hugging Face Transformers

\- \*\*Data Validation:\*\* Pydantic

\- \*\*Development Tools:\*\* Git, GitHub, VS Code, virtual environments





\## Repository Structure



genai-engineer-journey/

├── day01/

├── day02/

├── day03/

├── day04/

├── day05/

├── day06/

├── day07/

├── day08/

├── day09/

├── day10/

├── day11/

├── day12/

├── .gitignore

└── README.md





Each day's folder contains relevant code, exercises, and a dedicated README explaining the concepts and implementation.



\## Setup and Run



\### 1. Clone the repository

git clone https://github.com/YOUR\_USERNAME/genai-engineer-journey.git

cd genai-engineer-journey





Replace `YOUR\_USERNAME` with your GitHub username.

\### 2. Create and activate a virtual environment



On Windows using Git Bash:

python -m venv .venv

source .venv/Scripts/activate





\### 3. Install dependencies

Install the packages required by the project or learning day you want to run. Refer to that day's README and dependency instructions.



\### 4. Configure API credentials

Create a local `.env` file in the repository root when an exercise requires API access:



OPENAI\_API\_KEY=your\_api\_key\_here





Never commit `.env`, API keys, or other credentials to GitHub.



\### 5. Run a project



Navigate to the relevant day's folder and execute the Python script. For example:



cd day12

python llm\_change\_workflow.py





Some exercises require additional dependencies, a configured API key, or previously created local data.



\## Engineering Principles



\- Understand the fundamentals before relying on frameworks.

\- Keep code modular and maintainable.

\- Use structured outputs and validate model responses.

\- Ground RAG responses in retrieved context and expose source information.

\- Evaluate retrieval and answer quality rather than relying only on successful execution.

\- Treat LLM-generated decisions as recommendations unless validated by approved business rules.

\- Use human approval and appropriate safeguards for consequential enterprise operations.

\- Maintain code history and documentation using Git and GitHub.



\## Upcoming Goals



\- Build tool-calling applications and more capable agentic workflows.

\- Explore LangGraph state management, persistence, and human-in-the-loop patterns.

\- Develop a practical enterprise GenAI portfolio project.

\- Learn evaluation, tracing, guardrails, testing, and deployment.

\- Explore model adaptation and fine-tuning techniques where appropriate.

\- Prepare for GenAI Engineer technical interviews.





\## Disclaimer

This repository is an ongoing learning project. The examples are educational and are not intended to make autonomous production-change approvals or replace enterprise change-management policies.



\## Connect

This repository represents my practical learning journey toward a GenAI Engineer role. Feedback, suggestions, and constructive contributions are welcome.

