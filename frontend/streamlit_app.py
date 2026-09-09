import streamlit as st

from frontend.core.state import initialize_session_state
from frontend.core.sources import get_stored_sources
from frontend.features.ingestion.ui import render_ingestion
from frontend.features.query.ui import render_query
from frontend.i18n.language import setup_language


# Page configuration
st.set_page_config(
    page_title="Semantic Docs",
    page_icon="🗂️",
    layout="centered"
)

# get sources
get_stored_sources()

# Session State
initialize_session_state()

language, T = setup_language()

# PDF Upload Section
render_ingestion(T=T)

# Query Section
render_query(T=T)