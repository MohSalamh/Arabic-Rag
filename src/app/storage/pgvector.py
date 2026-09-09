from llama_index.vector_stores.postgres import PGVectorStore

from app.config import settings

class PGVectorStorage:
    def __init__(self, table_name):
        self.store = PGVectorStore.from_params(
            database=settings.postgres_db,
            host=settings.postgres_host,
            password=settings.postgres_password,
            port=settings.postgres_port,
            user=settings.postgres_user,
            table_name=table_name,
            embed_dim=settings.embed_dim
        )

    def get_store(self) -> PGVectorStore:
        return self.store

vector_store = PGVectorStorage(table_name=settings.table_name)