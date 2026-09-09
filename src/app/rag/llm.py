from llama_index.llms.openai import OpenAI
from llama_index.core.llms import ChatMessage, MessageRole

from app.config import settings
from app.models import RAGSearchResult, RAGQueryResult

RAG_SYSTEM_PROMPT = """ 
You are a helpful document question-answering assistant. 

Your job is to answer the user's question using only the provided document context. 

Follow these rules: 

1. Do not use information that is not present in the context. 
2. Do not make up or assume facts. 
3. If the context does not contain enough information to answer the question, clearly 
say that the answer cannot be found in the provided documents. 
4. Give a direct and concise answer. 
5. Preserve important names, numbers, dates, and technical terms.
6. If multiple parts of the context are relevant, combine them into a coherent answer. 
7. Do not mention the retrieval process or these instructions. 
""".strip()

RAG_USER_PROMPT = """ 
Answer the following question using only the provided document context. 

Document context:
 
{context} 

Question: 

{question} 
""".strip()

def build_context(contexts: list[str]) -> str:
    """ Combine retrieved document chunks into one context string. """
    return "\n\n---\n\n".join(context.strip() for context in contexts if context.strip())

def get_system_prompt() -> str:
    return RAG_SYSTEM_PROMPT

def build_user_prompt(question: str, contexts: list[str]) -> str:
    """ Build the user prompt with the question and retrieved context. """
    context = build_context(contexts)
    return RAG_USER_PROMPT.format(context=context, question=question)

def get_llm_model():
    llm_model = OpenAI(
        model=settings.llm_model,
        api_key=settings.openai_api_key
    )

    return llm_model

def get_llm_answer(question: str, retrieved_results: RAGSearchResult) -> RAGQueryResult:
    llm_model = get_llm_model()

    messages = [
        ChatMessage(
            role=MessageRole.SYSTEM,
            content=get_system_prompt()
        ),
        ChatMessage(
            role=MessageRole.USER,
            content=build_user_prompt(question, retrieved_results.contexts)
        ),
    ]

    response = llm_model.chat(messages)

    answer = response.message.content

    sources_metadata = retrieved_results.sources
    sources = set([source_metadata.source for source_metadata in sources_metadata])
    sources = list(sources)

    num_contexts = len(retrieved_results.contexts)

    rag_query_result = RAGQueryResult(
        answer=answer,
        sources=sources,
        num_contexts=num_contexts
    )

    return rag_query_result



