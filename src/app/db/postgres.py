import psycopg

from app.config import settings
from app.models import RAGStoredDocs

def establish_connection():
    conn = psycopg.connect(
        host=settings.postgres_host,
        port=settings.postgres_port,
        dbname=settings.postgres_db,
        user=settings.postgres_user,
        password=settings.postgres_password
    )

    return conn

def initialize_database() -> None:
    conn = establish_connection()

    with conn.cursor() as cur:
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector")

    conn.commit()
    conn.close()

def retrieve_stored_documents() -> RAGStoredDocs:
    conn = establish_connection()

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT metadata_->>'source'
                FROM data_documents_store
                WHERE metadata_->>'source' IS NOT NULL
                GROUP BY metadata_->>'source'
                ORDER BY metadata_->>'source';
            """)

            sources = [row[0] for row in cur.fetchall()]

    except psycopg.errors.UndefinedTable:
        sources = []

    finally:
        conn.close()

    return RAGStoredDocs(stored_docs=sources)

