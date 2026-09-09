import asyncio
import time
from typing import Any

import httpx
import inngest

from app.config import settings
from app.inngest_jobs.client import inngest_client


class InngestError(Exception):
    """Base exception for Inngest communication errors."""


class InngestRunFailed(InngestError):
    """Raised when an Inngest run fails or is cancelled."""


class InngestRunTimeout(InngestError):
    """Raised when an Inngest run does not complete in time."""


class InngestService:
    """
    Infrastructure service responsible for communicating with Inngest.

    This class knows about:
    - Inngest events
    - Inngest API
    - event IDs
    - run polling
    - Inngest run statuses

    It does NOT know anything about FastAPI or HTTPException.
    """

    def __init__(
        self,
        client: Any = inngest_client,
        api_base_url: str = settings.inngest_api_base_url,
    ):
        self.client = client
        self.api_base_url = api_base_url.rstrip("/")
        self.http_client = httpx.AsyncClient(
            timeout=httpx.Timeout(
                connect=30.0,
                read=30.0,
                write=30.0,
                pool=30.0,
            )
        )

    async def send_event(
        self,
        name: str,
        data: dict[str, Any],
    ) -> str:
        """
        Send an event to Inngest.

        Returns:
            The Inngest event ID.
        """
        result = await self.client.send(
            inngest.Event(
                name=name,
                data=data,
            )
        )

        return result[0]

    async def fetch_runs(
        self,
        event_id: str,
    ) -> list[dict[str, Any]]:
        """
        Fetch Inngest runs associated with an event.
        """
        url = f"{self.api_base_url}/events/{event_id}/runs"

        try:
            response = await self.http_client.get(url)
            response.raise_for_status()

        except httpx.HTTPError as exc:
            raise

        data = response.json()
        return data.get("data", [])

    async def wait_for_run(
        self,
        event_id: str,
        timeout_s: float = 120.0,
        poll_interval_s: float = 0.5,
    ) -> dict[str, Any]:
        """
        Wait for an Inngest workflow to complete.

        Returns:
            The output of the completed Inngest function.

        Raises:
            InngestRunFailed:
                If the workflow fails or is cancelled.

            InngestRunTimeout:
                If the workflow does not complete within timeout_s.
        """
        start = time.monotonic()
        last_status = None

        while True:
            runs = await self.fetch_runs(event_id)

            if runs:
                run = runs[0]
                status = run.get("status")

                if status:
                    last_status = status

                if status == "Completed":
                    return run.get("output") or {}

                if status in {
                    "Failed",
                    "Cancelled",
                }:
                    raise InngestRunFailed(
                        f"Inngest function run {status}"
                    )

            elapsed = time.monotonic() - start

            if elapsed > timeout_s:
                raise InngestRunTimeout(
                    "Timed out waiting for Inngest run. "
                    f"Last status: {last_status}"
                )

            await asyncio.sleep(poll_interval_s)

    async def send_and_wait(
        self,
        name: str,
        data: dict[str, Any],
        timeout_s: float = 120.0,
        poll_interval_s: float = 0.5,
    ) -> dict[str, Any]:
        """
        Send an event and wait for its workflow to complete.
        """
        event_id = await self.send_event(
            name=name,
            data=data,
        )

        return await self.wait_for_run(
            event_id=event_id,
            timeout_s=timeout_s,
            poll_interval_s=poll_interval_s,
        )


inngest_service = InngestService()
