import httpx
from fastapi import APIRouter, HTTPException

from app.inngest_jobs.inngest_service import inngest_service


RAG_SOURCE_EVENT = "rag/get_stored_docs"

db_router = APIRouter()


@db_router.post("")
async def get_sources():
    """
    Send a question to the Inngest RAG workflow
    and wait for the workflow result.
    """

    try:

        # --------------------------------------------------
        # Send question to Inngest &  Get event id
        # --------------------------------------------------

        event_id = await inngest_service.send_event(
            name=RAG_SOURCE_EVENT,
            data={}
        )

        # --------------------------------------------------
        # Return the actual RAG result
        # --------------------------------------------------

        return {
            "status": "processing",
            "event_id": event_id,
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