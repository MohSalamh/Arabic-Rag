import logging

import inngest
from inngest import PydanticSerializer

inngest_client = inngest.Inngest(
    app_id="arabic_rag_app",
    logger=logging.getLogger("uvicorn"),
    is_production=False,
    serializer=PydanticSerializer()
)
