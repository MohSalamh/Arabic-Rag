"""
Streamlit UI for the RAG query feature.
"""
import requests
import streamlit as st

from frontend.features.query.service import clean_context_sources, build_source_mapping, query_rag
from frontend.core.sources import get_stored_sources
from frontend.utils.inngest_status import display_inngest_run_status

# Query UI
def render_query(
    T: dict[str, str],
) -> None:
    """
    Render the complete RAG query interface.
    """
    # Section title
    st.divider()
    st.title(T["ask_title"])

    # Query form
    with st.form("rag_query_form"):

        try:
            # Get stored sources
            sources = get_stored_sources()

        except requests.RequestException as exc:
            st.error(f"{T['rag_query_failed']}: {exc}")
            sources = []

        # Build source mapping
        source_mapping = build_source_mapping(sources=sources, all_label=T["all"])
        source_options = list(source_mapping.keys())

        current_question = st.session_state.question_query

        current_top_k = st.session_state.top_k

        current_source = st.session_state.query_source
        if not current_source or current_source not in source_options:
            current_source = T["all"]

        # Question
        question = st.text_input(T["your_question"], value=current_question)

        # Top K
        top_k = st.number_input(
            T["chunks_to_retrieve"],
            min_value=1,
            max_value=20,
            value=current_top_k,
            step=1,
        )

        # Source selector
        selected_source = st.selectbox(
            T["select_source"],
            options=source_options,
            index=source_options.index(current_source),
        )

        st.session_state.question_query = question
        st.session_state.top_k = top_k
        st.session_state.query_source = selected_source

        # Translate display name into actual backend source
        source_filter = source_mapping[selected_source]

        # Submit
        submitted = st.form_submit_button(T["ask"])

    # Process query
    if submitted:

        # Validate question
        if not question.strip():
            st.warning(T["your_question"])
            return

        # Execute RAG query
        with st.spinner(
            T["sending_query"]
        ):
            try:
                # Status placeholder
                status_placeholder = st.empty()

                result = query_rag(
                    question=question.strip(),
                    top_k=int(top_k),
                    source=source_filter,
                    on_status_change=lambda status: display_inngest_run_status(
                        T=T, status=status, status_placeholder=status_placeholder)
                )

                # Save result in session state
                st.session_state.ingest_query_answer = result.get("answer")

                query_sources = clean_context_sources(sources=result.get("sources"))
                st.session_state.ingest_query_sources = query_sources

            except requests.RequestException as exc:
                status_placeholder.error(f"{T['rag_query_failed']}: {exc}")

            except ValueError:
                status_placeholder.error(T["invalid_json"])

            except RuntimeError:
                status_placeholder.error(T["rag_no_result"])

            except Exception as exc:
                status_placeholder.error(f"{T['unexpected_error']}: {exc}")

    # Display answer
    render_query_result(T=T)


# Query result
def render_query_result(T: dict[str, str]) -> None:
    """
    Display the latest RAG answer and its sources.
    """
    answer = st.session_state.ingest_query_answer
    query_sources = st.session_state.ingest_query_sources

    # Answer
    st.subheader(T["answer"])
    st.write(answer or T["no_answer"])

    # Sources
    if query_sources:
        st.caption(T["sources"])

        for source in query_sources:
            st.write(f"- {source}")
