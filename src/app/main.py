from fastapi import FastAPI
from inngest.fast_api import serve

from app.db.postgres import initialize_database

from app.inngest_jobs.client import inngest_client
from app.inngest_jobs.functions.ingest_pdf import rag_ingest_pdf
from app.inngest_jobs.functions.query_pdf import rag_query_pdf_ai
from app.inngest_jobs.functions.ingested_pdf import rag_get_stored_docs

from app.api.documents import ingest_router
from app.api.chat import chat_router
from app.api.inngest_status import status_router
from app.api.sources import db_router

from app.config import settings

initialize_database()

app = FastAPI(
    title=settings.app_name
)

# FastAPI routes
app.include_router(
    ingest_router,
    prefix="/ingest",
    tags=["PDF Ingestion"]
)

app.include_router(
    chat_router,
    prefix="/query",
    tags=["PDF Query"]
)

app.include_router(
    status_router,
    prefix="/status",
    tags=["Check Inngest Result"]
)

app.include_router(
    db_router,
    prefix="/sources",
    tags=["Get Vectorized Sources"]
)

@app.get("/health")
async def health():
    return {"status": "ok"}

serve(
    app,
    inngest_client,
    [rag_ingest_pdf, rag_query_pdf_ai, rag_get_stored_docs]
)