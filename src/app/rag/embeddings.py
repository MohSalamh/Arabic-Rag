from llama_index.core import Document, StorageContext, VectorStoreIndex
from llama_index.embeddings.openai import OpenAIEmbedding

from app.storage.pgvector import vector_store
from app.config import settings
from app.models import RAGUpsertResult


embed_model = OpenAIEmbedding(
    model=settings.embedding_model,
    api_key=settings.openai_api_key,
    dimensions=settings.embed_dim,
)

def create_documents(chunks):
    documents = [
        Document(
            text=chunk.text,
            metadata={
                "source_id": chunk.id,
                "page": chunk.page,
                "source": chunk.source,
            }
        )
        for chunk in chunks
    ]

    return documents

def embed_upsert_vectors(chunks):
    storage_context = StorageContext.from_defaults(vector_store=vector_store.get_store())

    documents = create_documents(chunks=chunks)

    VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        vector_store=vector_store.get_store(),
        embed_model=embed_model
    )

    num_ingested = len(documents)

    return RAGUpsertResult(ingested=num_ingested)

