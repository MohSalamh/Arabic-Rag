import datetime
import asyncio
import inngest

from app.inngest_jobs.client import inngest_client
from app.rag.loader import load_and_chunk_pdf
from app.rag.embeddings import embed_upsert_vectors
from app.models import RAGChunk, RAGUpsertResult
from app.config import settings

@inngest_client.create_function(
    fn_id="RAG, Ingest PDF",
    trigger=inngest.TriggerEvent(event="rag/ingest_pdf"),
    throttle=inngest.Throttle(limit=2, period=datetime.timedelta(minutes=1)),
    rate_limit=inngest.RateLimit(limit=1, period=datetime.timedelta(hours=4), key="event.data.pdf_path"),
)
async def rag_ingest_pdf(ctx: inngest.Context):

    pdf_path = ctx.event.data["pdf_path"]

    chunks = await ctx.step.run(
        "load-and-chunk",
        lambda: asyncio.to_thread(load_and_chunk_pdf, pdf_path),
        output_type=list[RAGChunk]
    )

    result = await ctx.step.run(
        "embed-and-upsert",
        lambda: asyncio.to_thread(
            embed_upsert_vectors, chunks
        ),
        output_type=RAGUpsertResult
    )

    return result.model_dump()