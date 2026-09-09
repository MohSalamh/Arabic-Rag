class Settings:
    """ Application settings for the streamlit frontend """

    # API endpoints

    api_base_url: str = "http://localhost:8000"
    inngest_url: str = "http://localhost:8288"

    # Timeouts
    api_timeout: int = 30
    sources_timeout: int = 120
    status_timeout: int = 10

    # Inngest polling
    polling_interval: float = float(0.2)
    polling_timeout: float = float(120)

    # File storage
    upload_directory: str = "rag_uploads"

    # API URL properties

    @property
    def ingest_url(self) -> str:
        """ URL used to trigger PDF ingestion """
        return f"{self.api_base_url}/ingest"

    @property
    def query_url(self) -> str:
        """ URL used to trigger RAG query """
        return f"{self.api_base_url}/query"

    @property
    def sources_url(self) -> str:
        """ URL used to trigger stored sources retrieval"""
        return f"{self.api_base_url}/sources"

    @property
    def fastapi_inngest_status_url(self) -> str:
        """ URL used to trigger RAG query """
        return f"{self.api_base_url}/status?event_id={{}}"

    @property
    def inngest_status_url(self) -> str:
        """ URL used to retrieve Inngest run status """
        return f"{self.inngest_url}/v1/events/{{}}/runs"


# Shared application settings instance
settings = Settings()