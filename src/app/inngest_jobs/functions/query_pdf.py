import inngest
import asyncio

from app.inngest_jobs.client import inngest_client

from app.rag.retriever import search_context_sources
from app.rag.llm import get_llm_answer

from app.models import RAGSearchResult, RAGQueryResult

from app.config import settings

@inngest_client.create_function(
    fn_id="RAG: Query PDF",
    trigger=inngest.TriggerEvent(event="rag/query_pdf_ai")
)
async def rag_query_pdf_ai(ctx: inngest.Context):
    question = ctx.event.data["question"]
    top_k = ctx.event.data.get("top_k") or 5

    # Metadata used to restrict retrieval
    metadata = {
        "source": ctx.event.data.get("source")
    }

    retrieved_results = await ctx.step.run(
        "embed-and-search",
        lambda: asyncio.to_thread(
            search_context_sources,
            question,
            top_k,
            metadata
        ),
        output_type=RAGSearchResult
    )

    response = await ctx.step.run(
        "llm-answer",
        lambda: asyncio.to_thread(get_llm_answer, question, retrieved_results),
        output_type=RAGQueryResult
    )

    return response.model_dump()