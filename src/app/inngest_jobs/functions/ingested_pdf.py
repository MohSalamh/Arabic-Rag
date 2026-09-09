import inngest

import asyncio

from app.inngest_jobs.client import inngest_client
from app.db.postgres import retrieve_stored_documents
from app.models import RAGStoredDocs


@inngest_client.create_function(
    fn_id="RAG: Stored Docs",
    trigger=inngest.TriggerEvent(event="rag/get_stored_docs")
)
async def rag_get_stored_docs(ctx: inngest.Context):

    stored_docs = await ctx.step.run(
        "get-stored-docs",
        lambda: asyncio.to_thread(retrieve_stored_documents),
        output_type=RAGStoredDocs
    )

    return stored_docs.model_dump()