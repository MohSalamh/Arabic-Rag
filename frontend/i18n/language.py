"""
Language selection and RTL/LTR support for Streamlit.
"""

import streamlit as st

from frontend.i18n.translations import get_translations


# Language configuration
LANGUAGE_OPTIONS = {
    "en": "English",
    "ar": "العربية",
}

# Language selector
def render_language_selector() -> str:
    """
    Render the language selector.

    Returns:
        Selected language code, e.g. "en" or "ar".
    """
    current_language = st.session_state.language

    language_codes = list(LANGUAGE_OPTIONS.keys())

    language_labels = list(LANGUAGE_OPTIONS.values())

    current_index = language_codes.index(current_language)

    selected_label = st.selectbox(
        "Language / اللغة",
        language_labels,
        index=current_index,
        key="language_selector",
    )

    # Convert displayed label back to language code
    selected_language = next(
        language_code
        for language_code, label
        in LANGUAGE_OPTIONS.items()
        if label == selected_label
    )

    # Language changed
    if selected_language != current_language:
        st.session_state.language = selected_language
        st.rerun()

    return selected_language


# RTL / LTR

def apply_language_css(language: str) -> None:
    """
    Apply RTL/LTR CSS based on the selected language.

    Arabic:
        direction = rtl
        text-align = right

    English:
        direction = ltr
        text-align = left
    """

    direction = "rtl" if language == "ar" else "ltr"
    text_align = "right" if language == "ar" else "left"

    st.markdown(
        f"""
        <style>

        /* =====================================================
           GLOBAL
           ===================================================== */

        .stApp {{
            direction: {direction} !important;
        }}

        .main {{
            direction: {direction} !important;
        }}

        .block-container {{
            direction: {direction} !important;
            text-align: {text_align} !important;
        }}


        /* =====================================================
           HEADINGS
           ===================================================== */

        h1,
        h2,
        h3 {{
            direction: {direction} !important;
            text-align: {text_align} !important;
            width: 100% !important;
        }}

        [data-testid="stHeading"] {{
            direction: {direction} !important;
            text-align: {text_align} !important;
            width: 100% !important;
        }}

        [data-testid="stHeading"] > div {{
            direction: {direction} !important;
            text-align: {text_align} !important;
            width: 100% !important;
        }}

        [data-testid="stHeading"] h1,
        [data-testid="stHeading"] h2,
        [data-testid="stHeading"] h3 {{
            direction: {direction} !important;
            text-align: {text_align} !important;
            width: 100% !important;
        }}


        /* =====================================================
           MARKDOWN
           ===================================================== */

        [data-testid="stMarkdownContainer"] {{
            direction: {direction} !important;
            text-align: {text_align} !important;
        }}

        [data-testid="stMarkdownContainer"] p {{
            direction: {direction} !important;
            text-align: {text_align} !important;
        }}


        /* =====================================================
           WIDGET LABELS
           ===================================================== */

        label {{
            direction: {direction} !important;
            text-align: {text_align} !important;
        }}

        [data-testid="stWidgetLabel"] {{
            direction: {direction} !important;
            text-align: {text_align} !important;
        }}

        [data-testid="stWidgetLabel"] p {{
            direction: {direction} !important;
            text-align: {text_align} !important;
        }}


        /* =====================================================
           TEXT INPUTS
           ===================================================== */

        input,
        textarea {{
            direction: {direction} !important;
            text-align: {text_align} !important;
        }}


        /* =====================================================
           SELECT BOX
           ===================================================== */

        div[data-baseweb="select"] {{
            direction: {direction} !important;
        }}

        div[data-baseweb="select"] > div {{
            direction: {direction} !important;
            text-align: {text_align} !important;
        }}


        /* =====================================================
           FILE UPLOADER
           ===================================================== */

        section[data-testid="stFileUploader"] {{
            direction: {direction} !important;
            text-align: {text_align} !important;
        }}

        section[data-testid="stFileUploader"] * {{
            direction: {direction} !important;
            text-align: {text_align} !important;
        }}


        /* =====================================================
           FORM
           ===================================================== */

        div[data-testid="stForm"] {{
            direction: {direction} !important;
            text-align: {text_align} !important;
        }}


        /* =====================================================
           BUTTONS
           ===================================================== */

        button {{
            direction: {direction} !important;
        }}


        /* =====================================================
           ALERTS
           ===================================================== */

        div[data-testid="stAlert"] {{
            direction: {direction} !important;
            text-align: {text_align} !important;
        }}

        div[data-testid="stAlert"] * {{
            direction: {direction} !important;
            text-align: {text_align} !important;
        }}


        /* =====================================================
           CAPTIONS
           ===================================================== */

        [data-testid="stCaptionContainer"] {{
            direction: {direction} !important;
            text-align: {text_align} !important;
        }}


        /* =====================================================
           SPINNER
           ===================================================== */

        div[data-testid="stSpinner"] {{
            direction: {direction} !important;
            text-align: {text_align} !important;
        }}

        div[data-testid="stSpinner"] * {{
            direction: {direction} !important;
            text-align: {text_align} !important;
        }}


        /* =====================================================
           CODE / TECHNICAL CONTENT
           ===================================================== */

        code,
        pre {{
            direction: ltr !important;
            text-align: left !important;
        }}


        /* =====================================================
           TABLES
           ===================================================== */

        table {{
            direction: {direction} !important;
        }}

        th,
        td {{
            text-align: {text_align} !important;
        }}


        /* =====================================================
           MOBILE
           ===================================================== */

        @media (max-width: 768px) {{

            .block-container {{
                padding-left: 1rem;
                padding-right: 1rem;
            }}

            h1 {{
                font-size: 1.8rem !important;
            }}

            h2 {{
                font-size: 1.4rem !important;
            }}

        }}

        </style>
        """,
        unsafe_allow_html=True,
    )


# Main language setup
def setup_language() -> tuple[str, dict[str, str]]:
    """
    Initialize language, render the language selector,
    apply RTL/LTR CSS, and return the current translations.
    """
    language = render_language_selector()

    apply_language_css(language)

    translations = get_translations(language)

    return language, translations
