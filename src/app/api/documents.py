import httpx
from fastapi import APIRouter, HTTPException

from app.inngest_jobs.inngest_service import inngest_service

from pathlib import Path

RAG_INGEST_EVENT = "rag/ingest_pdf"

ingest_router = APIRouter()

@ingest_router.post("")
async def document_ingestion(pdf_path: str):
    """ trigger the Inngest PDF ingestion workflow. """

    # -----------------------------------------
    # Validate file
    # -----------------------------------------

    path = Path(pdf_path)

    if not path.name:
        raise HTTPException(status_code=400, detail="Filename is required.")

    if not path.is_file():
        raise HTTPException(status_code=404, detail="PDF file not found.")

    if not path.name.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:

        # -----------------------------------------
        # Send event to Inngest
        # -----------------------------------------

        event_id = await inngest_service.send_event(
            name=RAG_INGEST_EVENT,
            data={"pdf_path": pdf_path}
        )

        # -----------------------------------------
        # Return response
        # -----------------------------------------

        return {
            "status": "processing",
            "event_id": event_id,
            "filename": path.name,
        }

    except TimeoutError as exc:

        raise HTTPException(
            status_code=504,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    except httpx.HTTPError as exc:

        raise HTTPException(
            status_code=502,
            detail=(
                "Failed to communicate with "
                f"Inngest API: {str(exc)}"
            ),
        ) from exc

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

'''
@ingest_router.get("/status/{event_id}")
async def check_ingestion_status(event_id: str):
    """Return the current status of an Inngest ingestion job."""

    try:
        runs = await inngest_service.fetch_runs(event_id)

        if not runs:
            return {
                "status": "Pending",
                "event_id": event_id,
            }

        run = runs[0]

        return {
            "status": run.get("status"),
            "event_id": event_id,
            "result": run.get("output"),
        }

    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to communicate with Inngest API: {exc}",
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc
'''



