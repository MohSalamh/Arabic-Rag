"""
Application translations.

Supported languages:
    en - English
    ar - Arabic
"""
from typing import Final

# Translations
TRANSLATIONS: Final[dict[str, dict[str, str]]] = {

    # English
    "en": {
        # Language
        "language": "Language",
        "language_english": "English",
        "language_arabic": "العربية",

        # PDF upload
        "upload_title": "Upload a PDF to Ingest",
        "choose_pdf": "Choose a PDF",
        "uploading": "Uploading and triggering ingestion...",

        # Status
        "status": "Status",
        "operation_completed": "Operation completed successfully.",
        "operation_failed": "Operation failed",
        "operation_status": "Operation status",
        "status_retry": (
            "⚠️ Could not contact the status endpoint. "
            "Retrying..."
        ),

        # Ingestion
        "ingestion_failed": "Failed to trigger ingestion",
        "ingestion_complete": "Ingestion for",
        "chunks_ingested": "Chunks ingested",
        "upload_another": "You can upload another PDF if you like.",

        # RAG query
        "ask_title": "Ask a question about your PDFs",
        "your_question": "Your question",
        "chunks_to_retrieve": "How many chunks to retrieve",
        "select_source": "Select Source",
        "all": "All",
        "ask": "Ask",
        "sending_query": "Sending event and generating answer...",
        "rag_query_failed": "Failed to query RAG API",
        "invalid_json": "The API returned invalid JSON.",
        "rag_no_result": "Could not get a result from the RAG service.",

        # RAG Result
        "answer": "Answer",
        "no_answer": "(No answer)",
        "sources": "Sources",
        "failed_processing": "Could not complete PDF processing.",

        # General Errors
        "unexpected_error": "Unexpected error",
    },

    # Arabic
    "ar": {
        # Language
        "language": "اللغة",
        "language_english": "English",
        "language_arabic": "العربية",

        # PDF upload
        "upload_title": "رفع ملف PDF لمعالجته",
        "choose_pdf": "اختر ملف PDF",
        "uploading": "جارٍ رفع الملف وبدء المعالجة...",

        # Status
        "status": "الحالة",
        "operation_completed": "تمت العملية بنجاح.",
        "operation_failed": "فشلت العملية",
        "operation_status": "حالة العملية",
        "status_retry": (
            "⚠️ تعذر الاتصال بخدمة متابعة الحالة. "
            "جارٍ إعادة المحاولة..."
        ),

        # Ingestion
        "ingestion_failed": "فشل بدء معالجة الملف",
        "ingestion_complete": "تمت معالجة الملف بنجاح",
        "chunks_ingested": "عدد المقاطع التي تمت معالجتها",
        "upload_another": "يمكنك رفع ملف PDF آخر إذا رغبت.",

        # RAG query
        "ask_title": "اطرح سؤالاً حول ملفات PDF",
        "your_question": "سؤالك",
        "chunks_to_retrieve": "عدد المقاطع المطلوب استرجاعها",
        "select_source": "اختر المصدر",
        "all": "الكل",
        "ask": "اسأل",
        "sending_query": (
            "جارٍ إرسال الطلب وإنشاء الإجابة..."
        ),
        "rag_query_failed": "فشل إرسال الاستعلام إلى واجهة RAG",
        "invalid_json": "أعادت واجهة API بيانات JSON غير صالحة.",
        "rag_no_result": "تعذر الحصول على نتيجة من خدمة RAG.",

        # RAG Result
        "answer": "الإجابة",
        "no_answer": "لم يتم العثور على إجابة.",
        "sources": "المصادر",
        "failed_processing": "تعذر إكمال معالجة الملف.",

        # General Error
        "unexpected_error": "حدث خطأ غير متوقع",
    }
}

SUPPORTED_LANGUAGES: Final[tuple[str, ...]] = (
    "en", "ar",
)

def get_translations(language: str) -> dict[str, str]:
    """ Return the translation dictionary for a language. """
    if language not in TRANSLATIONS:
        raise ValueError(f"Unsupported language: {language}")

    return TRANSLATIONS[language]