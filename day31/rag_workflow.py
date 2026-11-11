from typing import TypedDict,Literal
from dotenv import load_dotenv
import os
import json

from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph,START,END

load_dotenv("../.env")

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OpenAI API key not found")

embeddings=OpenAIEmbeddings(
    model="text-embedding-3-small"
)

llm=ChatOpenAI(
    model="gpt-6-astra",
    temperature=1
)

vectorstore=Chroma(
    collection_name="Change_management",
    embedding_function=embeddings,
    persist_directory="../day08/chroma_db"
)
print("Chroma db connected successfully")

class RAGState(TypedDict):
    question : str
    route : str
    documents : list
    answer : str
    context_status : str
    context_reason : str


prompt_router=ChatPromptTemplate.from_template(
"""
You are an intelligent Enterprise Change Management
RAG assistant.

Classify the question into exactly one category:

VECTOR_SEARCH:
For conceptual questions requiring semantic retrieval.

METADATA_FILTER:
For questions requesting specific records using
category, type or source metadata.

MULTI_QUERY:
For complex or broad questions requiring multiple
alternative searches.

Return only one category name.

Question: {question}
"""
)

router=prompt_router | llm | StrOutputParser()

metadata_prompt=ChatPromptTemplate.from_template(
"""
You are a metadata extraction assistant.

Available metadata fields and values:

category:
- Change Management
- Release Management

type:
- Procedure

source:
- normal_change
- emergency_change
- cab
- rollback
- production_validation
- change_closure
- release_planning
- build_and_packaging
- deployment_strategy
- staging_and_uat
- release_cutover

Extract relevant metadata filters from the user question.

Return valid JSON only.

Example:
{{
    "filter": {{
        "category": "Change Management"
    }}
}}

If multiple conditions exist, return them as separate
key-value pairs inside filter.

If no metadata filter is appropriate, return:
{{"filter": null}}

User question: {question}
"""
)

metadata_chain= metadata_prompt | llm | StrOutputParser()


multi_query_prompt=ChatPromptTemplate.from_template("""
You are an expert enterprise Change Management assistant.

Generate 3 alternative search queries for the user's question.

Each query should express the same intent using
different terminology or wording.

Return only the 3 queries, one per line.
Do not provide explanations or numbering.

User question: {question}
""")

query_generator=multi_query_prompt | llm | StrOutputParser()


context_check_prompt=ChatPromptTemplate.from_template("""
You are an enterprise RAG context evaluator.

Evaluate whether the retrieved context contains enough
relevant information to answer the user's question.

Return exactly one of these classifications:

SUFFICIENT:
The context contains enough information to answer
the question accurately.

INSUFFICIENT:
The context is missing important information or
does not adequately support an answer.

Question:
{question}

Retrieved Context:
{context}

Return your response in this format:

Status: SUFFICIENT or INSUFFICIENT
Reason: Brief explanation
""")

context_check_chain=context_check_prompt | llm | StrOutputParser()

def query_router(state : RAGState):
    route=router.invoke({
        "question" : state["question"]
    }).strip().upper()

    if route not in {
        "VECTOR_SEARCH",
        "METADATA_FILTER",
        "MULTI_QUERY"
    }:
        route="VECTOR_SEARCH"

    print("\nselected route :",route)

    return {"route" : route}

def vector_search_node(state : RAGState):
    print("Executing chromadb vector search....")

    question=state["question"]

    documents=vectorstore.similarity_search(
        question,
        k=5
    )

    print(f"retrieved {len(documents) } documents")

    for index,doc in enumerate(documents,start=1):
        print(f"\nDocument {index} :")
        print("Source : ",doc.metadata.get("source"))
        print("Content : ",doc.page_content[:250])

    return {"documents" : documents}

def metadata_filter_node(state : RAGState):
    print("Executing metadata chromadb retrieval.....")
    question=state["question"]
    try:
        
        response=metadata_chain.invoke({
            "question": question
        })

        result=json.loads(response)
        metadata_filter=result["filter"]
        print("Extracted filter:", metadata_filter)

        if not isinstance(metadata_filter,dict) or not metadata_filter:
            print("no metadata filter generated.....")
            return {"documents" : []}

        stored_metadata=vectorstore.get()["metadatas"]

        allowed_values={}

        for metadata in stored_metadata:
            for key,value in metadata.items():
                allowed_values.setdefault(key,set()).add(value)

        for key,value in metadata_filter.items():
            if key not in allowed_values:
                print(f"Unsupported metadata fieled: {key}")

            if value not in allowed_values[key]:
                raise ValueError(f"Unsupported metadata value {key}={value}")


        if len(metadata_filter)>1:
            metadata_filter={
                "$and": [
                    {key : value } for key, value in metadata_filter.items()
                ]
            }

        documents=vectorstore.similarity_search(
            question,
            k=5,
            filter=metadata_filter
        )
        print(f"Metadata filter retrieved {len(metadata_filter)} documents")

        for index,doc in enumerate(documents,start=1):
            print(f"Document {index} :")
            print("Source :",doc.metadata.get("source"))
            print("Category :",doc.metadata.get("category"))
            print("Content :",doc.page_content[:200])

        return {"documents" : documents}

    except(ValueError,TypeError,json.JSONDecodeError) as error:
        print("Metadata retrieval failed ",{error})
        print("allowing fallback to vector search")

        return {"documents" : []}



def reciprocal_rank_fusion(results,k=60):
    rrf_scores={}
    document_store={}
    for result_list in results:
        for rank,doc in enumerate(result_list,start=1):
            doc_id=doc.page_content

            if doc_id not in rrf_scores:
                rrf_scores[doc_id]=0
                document_store[doc_id]=doc

            rrf_scores[doc_id]=1/(k+rank)

    ranked_documents=sorted(
        rrf_scores.items(),
        key=lambda x:x[1],
        reverse=True
    )

    return [(document_store[doc_id],score) for doc_id,score in ranked_documents]


def multi_query_node(state: RAGState):
    print("Executing multi-query retrieval.....")

    question=state["question"]
    response=query_generator.invoke({
        "question" : question
    })

    generated_queries=[
        query.strip() for query in response.splitlines()
        if query.strip()
    ][:3]

    all_queries=[question]+generated_queries

    print("--------Generated_queries------------")
    for index,query in enumerate(all_queries,start=1):
        print(f"{index}.{query}")

    retrieval_results=[]

    for query in all_queries:
        print(f"Searching {query}")
        documents=vectorstore.similarity_search(
            question,
            k=5
        )

        retrieval_results.append(documents)

    fused_results=reciprocal_rank_fusion(retrieval_results)

    final_documents=[doc for doc,score in fused_results[:5]]

    print("--------rrf documents----------")

    for index,(doc,score) in enumerate(fused_results[:5],start=1):
        print(f"\nRank : {index}")
        print("Source : ",doc.metadata.get("source"))
        print("RRF Score : ",round(score,5))
        print("Content : ",doc.page_content[:200])

    return {"documents" : final_documents}



    print(f"Retrived {len(documents)} documents")
    return {"documents" : documents}





answer_prompt=ChatPromptTemplate.from_template("""
You are an Enterprise Change Management AI Assistant.

Answer the user's question using ONLY the provided context.

Instructions:
1. Do not invent information.
2. Do not use external knowledge.
3. If the context does not contain sufficient information,
   clearly state that you don't have sufficient information.
4. Provide a clear and structured answer.
5. Include source document names supporting your answer.
6. Cite sources using this format:
   [Source: document_name]
7. Only cite documents that actually support the claims.
8. Do not claim that a procedure is approved unless
   the context explicitly confirms it.

Context:
{context}

User Question:
{question}

Answer:
""")

answer_chain=answer_prompt | llm | StrOutputParser()

def answer_node(state:RAGState):
    print("Generating grounded answer........")

    question=state["question"]
    documents=state["documents"]

    if not documents:
        return {
            "answer" : "I don't have sufficient information in the knowledge base to answer this question."
        }

    context_parts=[]

    for doc in documents:
        source=doc.metadata.get("source","unknown")

        context_parts.append(
            f""" source : {source},
            content : {doc.page_content}
            """
        )
    context="\n\n".join(context_parts)

    answer=answer_chain.invoke({
            "question" : question,
            "context" : context
        })

    print("------------- Final Answer -----------------")
    print(answer)

    return {
        "answer" : answer
    }

def context_check_node(state:RAGState):
    print("\n\n-----Evaluating retrieved context--------")

    context="\n\n".join(
        [
            f"source : {doc.metadata.get('source')}\n"
            f"content : {doc.page_content}"
            for doc in state["documents"]
        ]
    )

    result=context_check_chain.invoke({
        "question":state["question"],
        "context": context
    })

    print(result)

    status_line=next(
        (line for line in result.splitlines()
         if line.strip().upper().startswith("STATUS:") 
         ),
         ""
    )

    status=(
        "SUFFICIENT"
        if "SUFFICIENT" in status_line.upper()
        and "INSUFFICIENT" not in status_line.upper()
        else "INSUFFICIENT"
    )

    return {
        "context_status" : status,
        "context_reason" : result
    }

def check_metadata_result(state:RAGState):
    if not state["documents"]:
        print("No metadata results. Falling ack to vector search")
        return "vector"
    print("Metadata results found, continuing to generate the answer")
    return "answer"

def select_retriever(state : RAGState) ->Literal["vector","metadata","multi"]:
    routes={
        "VECTOR_SEARCH" : "vector",
        "METADATA_FILTER" : "metadata",
        "MULTI_QUERY":"multi"
    }

    return routes.get(state["route"],"vector")

def check_context_status(state:RAGState):
    if state["context_status"]=="SUFFICIENT":
        print("Context is sufficient.Generating the answer...")
        return "answer"
    print("Context is insufficient. Returning safe answer...")
    return "insufficient"

def insufficient_context_node(state:RAGState):
    return {
        "answer" : (
            "I don't have sufficient information in the "
            "knowledge base to answer this question reliably. "
            "Please consult the relevant approved documentation."
        )
    }

workflow=StateGraph(RAGState)

workflow.add_node("router",query_router)
workflow.add_node("vector", vector_search_node)
workflow.add_node("metadata",metadata_filter_node)
workflow.add_node("multi",multi_query_node)
workflow.add_node("answer",answer_node)
workflow.add_node("context_check",context_check_node)
workflow.add_node("insufficient",insufficient_context_node)

workflow.add_edge(START,"router")

workflow.add_conditional_edges(
    "router",
    select_retriever,
    {
        "vector" : "vector",
        "metadata":"metadata",
        "multi":"multi"
    }
)

workflow.add_conditional_edges(
    "metadata",
    check_metadata_result,
    {
        "vector" : "vector",
        "answer" : "context_check"
    }
)

workflow.add_edge("vector","context_check")
workflow.add_edge("multi","context_check")

workflow.add_conditional_edges(
    "context_check",
    check_context_status,
    {
        "answer":"answer",
        "insufficient":"insufficient"
    }
)
workflow.add_edge("insufficient",END)
workflow.add_edge("answer",END)

app=workflow.compile()

questions=[
    "What is the rollback procedure?",
    "Find emergency changes related to SAP in production.",
    "Compare recovery procedures for failed production deployments."
]

for question in questions:
    print("\n------------------------")
    print("question :",question)

    result=app.invoke(
        {
            "question" : question,
            "route" : "",
            "documents": [],
            "answer":"",
            "context_status" :"",
            "context_reason":""
        }
    )

    print("\nFinal route:", result["route"])
    print("Retrieved document count:", len(result["documents"]))

    for index, doc in enumerate(result["documents"], start=1):
        print(f"\nDocument {index}")
        if isinstance(doc,list):
            print("unexpected nested list detected")
            continue
        print("Source:", doc.metadata.get("source"))
        print("Content:", doc.page_content[:200])
        print("\nFinal Answer:")
        print(result["answer"])