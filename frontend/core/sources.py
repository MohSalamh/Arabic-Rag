import streamlit as st

from frontend.core.api import trigger_sources
from frontend.core.polling import poll_inngest

@st.cache_data
def get_stored_sources():
    output_sources = trigger_sources()
    output_sources.raise_for_status()

    sources_event_id = output_sources.json()["event_id"]

    if not sources_event_id:
        raise ValueError("The sources API response did not contain an event_id."
        )

    result_sources = poll_inngest(
        event_id=sources_event_id,
    )

    if not result_sources:
        return []

    sources = result_sources.get("stored_docs", [])

    return sources