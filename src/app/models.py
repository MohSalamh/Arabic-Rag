import pydantic

class RAGChunk(pydantic.BaseModel):
    id: str
    text: str
    page: int
    source: str

class RAGUpsertResult(pydantic.BaseModel):
    ingested: int

class RagNodeMetadata(pydantic.BaseModel):
    source: str
    page: int
    score: float

class RAGSearchResult(pydantic.BaseModel):
    contexts: list[str]
    sources: list[RagNodeMetadata]

class RAGQueryResult(pydantic.BaseModel):
    answer: str
    sources: list[str]
    num_contexts: int

class RAGStoredDocs(pydantic.BaseModel):
    stored_docs: list[str] = []