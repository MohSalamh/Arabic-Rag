import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.inngest_jobs.inngest_service import inngest_service

from typing import Optional

RAG_QUERY_EVENT = "rag/query_pdf_ai"

chat_router = APIRouter()

class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
    )

    source: Optional[str] = Field(
        default=None,
    )



@chat_router.post("")
async def chat(
    request: ChatRequest,
):
    """
    Send a question to the Inngest RAG workflow
    and wait for the workflow result.
    """

    try:

        # --------------------------------------------------
        # Send question to Inngest &  Get event id
        # --------------------------------------------------

        event_id = await inngest_service.send_event(
            name=RAG_QUERY_EVENT,
            data={"question": request.question, "top_k": request.top_k, "source": request.source}
        )

        # --------------------------------------------------
        # Return the actual RAG result
        # --------------------------------------------------

        return {
            "status": "processing",
            "event_id": event_id,
            "question": request.question
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
@chat_router.get("/status/{event_id}")
async def check_response_status(event_id: str):
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