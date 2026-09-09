"""
RAG query service.
"""
import re
from typing import Any
from collections.abc import Callable

from frontend.core.api import trigger_query
from frontend.core.polling import poll_inngest

StatusCallback = Callable[[str], None]

def clean_source_name(source: str) -> str:
    """
    Remove the UUID prefix from a stored source filename.

    Example:
        550e8400-e29b-41d4-a716-446655440000_report.pdf

    becomes:
        report.pdf
    """

    return re.sub(r"^[0-9a-fA-F-]{36}_", "", source,)

def clean_context_sources(sources: list[str] | None=None) -> list[str] | None:
    if not sources:
        return []

    clean_sources = list(dict.fromkeys(
        clean_source_name(source)
        for source in sources
    ))
    return clean_sources

def build_source_mapping(sources: list[str], all_label: str) -> dict[str, str | None]:
    """
    Build a mapping between display names and stored source names.

    The UI displays the clean filename, while the backend receives the actual stored filename.
    """
    source_mapping: dict[str, str | None] = {
        all_label: None,
    }

    for source in sources:
        clean_name = clean_source_name(source)

        # If duplicate clean names exist, preserve the
        # first one encountered.
        if clean_name not in source_mapping:
            source_mapping[clean_name] = source

    return dict(
        sorted(
            source_mapping.items(),
            key=lambda item: (
                item[0] != all_label,
                item[0].lower(),
            ),
        )
    )

# RAG query
def query_rag(
    question: str,
    top_k: int,
    source: str | None,
    on_status_change: StatusCallback | None = None,
) -> dict[str, Any]:
    """
    Submit a question to the RAG backend and wait for the
    asynchronous Inngest workflow to complete.
    """

    # Trigger RAG query
    response = trigger_query(
        question=question,
        top_k=top_k,
        source=source,
    )

    response.raise_for_status()

    data = response.json()

    event_id = data.get("event_id")

    if not event_id:
        raise ValueError(
            "The query API response did not contain an event_id."
        )

    # Wait for asynchronous RAG workflow
    result = poll_inngest(
        event_id=event_id,
        on_status_change=on_status_change,
    )

    if not result:
        raise RuntimeError("The RAG query failed or timed out.")

    return result
