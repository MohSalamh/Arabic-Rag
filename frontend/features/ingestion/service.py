from pathlib import Path
from typing import Any
from collections.abc import Callable

from frontend.core.api import trigger_ingestion
from frontend.core.polling import poll_inngest
from frontend.utils.files import save_uploaded_pdf


StatusCallback = Callable[[str], None]

def ingest_pdf(
        uploaded_file: Any,
        on_status_change: StatusCallback | None = None
) -> dict[str, Any]:
    """
    Save a PDF, trigger the ingestion workflow, and wait for completion.
    """

    # Save uploaded PDF
    pdf_path, clean_name = save_uploaded_pdf(uploaded_file)

    # Trigger ingestion
    response = trigger_ingestion(pdf_path=pdf_path)

    response.raise_for_status()

    data = response.json()

    event_id = data.get("event_id")

    if not event_id:
        raise ValueError(
            "The ingestion API response did not contain an event_id."
        )

    # Wait for Inngest workflow
    result = poll_inngest(event_id=event_id, on_status_change=on_status_change)

    if not result:
        raise RuntimeError("PDF ingestion failed or timed out.")

    # Return normalized result
    return {
        "path": Path(pdf_path),
        "filename": clean_name,
        "chunks_ingested": result.get("ingested"),
        "raw_result": result,
    }