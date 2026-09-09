import streamlit as st


DEFAULT_STATE = {
    "language": "en",
    "uploader_key": 0,
    "ingestion_filename": None,
    "ingest_chunks_ingested": None,
    "ingest_query_answer": None,
    "ingest_query_sources": None,
    "question_query": "",
    "top_k": 5,
    "query_source": None
}


def initialize_session_state():
    for key, value in DEFAULT_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = value