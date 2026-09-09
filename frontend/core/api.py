import requests
from pathlib import Path

from frontend.config.settings import settings

def trigger_ingestion(pdf_path: Path):
    """
    Trigger the ingestion workflow.
    This request should return quickly with an event_id.
    It does NOT wait for the PDF to finish processing.
    """

    response = requests.post(
        settings.ingest_url,
        params={"pdf_path": str(pdf_path)},
        timeout=settings.api_timeout
    )

    return response

def trigger_query(question: str, top_k: int, source: str | None):
    """Send a RAG query to FastAPI and get the event id"""
    response = requests.post(
        settings.query_url,
        json={
            "question": question,
            "top_k": top_k,
            "source": source
        },
        timeout=settings.api_timeout
    )

    return response

def trigger_sources():
    """Send a get stored sources event to FastAPI and get the event id"""
    response = requests.post(
        settings.sources_url,
        json={},
        timeout=settings.api_timeout
    )

    return response

def fastapi_get_inngest_run(event_id: str):
    """ Get the current Inngest ingestion status """
    response = requests.get(
        settings.fastapi_inngest_status_url.format(event_id), timeout=settings.status_timeout
    )
    response.raise_for_status()

    return response.json()

def get_inngest_run(event_id: str):
    """ Get the current Inngest ingestion status """
    response = requests.get(
        settings.inngest_status_url.format(event_id), timeout=settings.status_timeout
    )
    response.raise_for_status()

    data = response.json()

    result = data.get("data", [])

    return result[0] if result else {}

