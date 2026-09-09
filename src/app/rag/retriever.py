from llama_index.core import VectorStoreIndex
from llama_index.core.vector_stores import MetadataFilter, MetadataFilters

from app.storage.pgvector import vector_store
from app.rag.embeddings import embed_model

def build_metadata_filters(
    metadata: dict[str, object] | None,
) -> MetadataFilters | None:

    if not metadata:
        return None

    return MetadataFilters(
        filters=[
            MetadataFilter(
                key=key,
                value=value,
            )
            for key, value in metadata.items() if value is not None
        ]
    )

def get_index() -> VectorStoreIndex:
    """ Create a LlamaIndex index backed by PostgreSQL/pgvector. """
    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store.get_store(),
        embed_model=embed_model
    )
    return index

def get_retriever(
        top_k: int = 5,
        metadata: dict[str, object] | None = None
):
    """ Create a retriever for the configured vector store. """
    index = get_index()
    metadata_filters = build_metadata_filters(metadata)
    retriever = index.as_retriever(similarity_top_k=top_k, filters=metadata_filters)
    return retriever

def retrieve(
        question: str,
        top_k: int = 5,
        metadata: dict[str, object] | None = None
):
    """ Retrieve the most relevant document chunks for a question. """
    if not question.strip():
        raise ValueError("Question cannot be empty.")
    retriever = get_retriever(
        top_k=top_k,
        metadata=metadata
    )
    nodes = retriever.retrieve(question)
    return nodes

def search_context_sources(
        question: str,
        top_k: int=5,
        metadata: dict[str, object] | None = None
) -> dict:
    """ Retrieve relevant chunks and convert them into application-friendly context and source data. """
    nodes = retrieve(question=question, top_k=top_k, metadata=metadata)
    contexts = []
    sources = []
    for result in nodes:
        node = result.node
        contexts.append(node.get_content())
        sources.append(
            {
                "source": node.metadata.get("source"),
                "page": node.metadata.get("page"),
                "score": result.score
            }
        )
    return {"contexts": contexts, "sources": sources}