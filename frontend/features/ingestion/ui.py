"""
Streamlit UI for PDF ingestion.
"""
import requests
import streamlit as st

from frontend.features.ingestion.service import ingest_pdf
from frontend.utils.inngest_status import display_inngest_run_status

def render_ingestion(T: dict[str, str]) -> None:
    """
    Render the PDF upload and ingestion section.

    Args:
        T:
            Translation dictionary for the current language.
    """

    # Section title
    st.title(T["upload_title"])

    # PDF uploader
    uploaded_file = st.file_uploader(
        T["choose_pdf"],
        type=["pdf"],
        accept_multiple_files=False,
        key=(
            f"pdf_uploader_"
            f"{st.session_state.uploader_key}"
        ),
    )

    # Nothing uploaded yet.
    if uploaded_file is None:
        # Display ingestion status
        render_ingestion_result(T=T)
        return

    # Process uploaded PDF
    with st.spinner(
        T["uploading"]
    ):

        try:
            status_placeholder = st.empty()

            result = ingest_pdf(
                uploaded_file,
                on_status_change=lambda status: display_inngest_run_status(
                    T=T, status=status, status_placeholder=status_placeholder)
            )

            # Store ingestion result in session state
            st.session_state.ingestion_filename = result["filename"]
            st.session_state.ingest_chunks_ingested = result["chunks_ingested"]

            # Allow the same uploader to select another file.
            st.session_state.uploader_key += 1

            # Sources have changed after ingestion.
            # Clear cached sources so the newly ingested PDF becomes available immediately.
            _clear_sources_cache()

            # Rerun so the uploader resets and the ingestion
            # result is displayed.
            st.rerun()

        except requests.RequestException as exc:
            st.error(f"{T['ingestion_failed']}: {exc}")

        except ValueError as exc:
            st.error(f"{T['unexpected_error']}: {exc}")

        except RuntimeError:
            st.error(T["failed_processing"])

        except Exception as exc:
            st.error(f"{T['unexpected_error']}: {exc}")


def render_ingestion_result(T: dict[str, str]) -> None:
    """
    Display the result of the most recent PDF ingestion.
    """
    chunks_ingested = st.session_state.ingest_chunks_ingested

    # No ingestion result to display.
    if chunks_ingested is None:
        return

    filename = st.session_state.ingestion_filename

    # Success message
    st.success(f"{T['ingestion_complete']}: {filename}")

    # Number of chunks
    st.success(f"📚 {T['chunks_ingested']}: **{chunks_ingested}**")

    # Additional information
    st.caption(T["upload_another"])


def _clear_sources_cache() -> None:
    """
    Clear the cached document-source list.
    """

    try:
        from frontend.core.sources import get_stored_sources
        get_stored_sources.clear()
    except ImportError:
        # Query feature may not exist yet.
        pass
