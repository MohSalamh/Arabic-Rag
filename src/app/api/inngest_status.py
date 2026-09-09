import httpx
from fastapi import APIRouter, HTTPException
from app.inngest_jobs.inngest_service import inngest_service

status_router = APIRouter()

@status_router.get("")
async def check_status(event_id: str):
    """Return the current status of an Inngest job."""

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
            "output": run.get("output"),
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

