import time
import requests
from collections.abc import Callable

from frontend.core.api import get_inngest_run, fastapi_get_inngest_run
from frontend.config.settings import settings


ACTIVE_STATUSES = {
    "Pending",
    "Running",
    "Started",
    "Queued",
}

SUCCESS_STATUSES = {
    "Completed",
    "Succeeded",
    "Success",
    "Finished",
}

FAILED_STATUSES = {
    "Failed",
    "Cancelled",
}


def poll_inngest(
    event_id: str,
    poll_interval: float = settings.polling_interval,
    timeout: float = settings.polling_timeout,
    on_status_change: Callable[[str], None] | None = None

):
    start = time.monotonic()

    while time.monotonic() - start <= timeout:
        try:
            data = fastapi_get_inngest_run(event_id)
            status = data.get("status", "Unknown")

            # Notify the caller about the status.
            if on_status_change:
                on_status_change(status)

            if status in ACTIVE_STATUSES:
                time.sleep(poll_interval)
                continue

            if status in SUCCESS_STATUSES:
                result = data.get("output") or {}

                # Wait for output if it isn't available yet.
                if not result:
                    time.sleep(poll_interval)
                    continue

                return result

            if status in FAILED_STATUSES:
                return None

            # Unknown status
            time.sleep(poll_interval)

        except requests.RequestException:
            if on_status_change:
                on_status_change("ConnectionError")

            time.sleep(poll_interval)

    return None