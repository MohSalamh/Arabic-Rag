from llama_index.readers.file import PDFReader
from llama_index.core.node_parser import SentenceSplitter

import uuid
from pathlib import Path
import time

def load_and_chunk_pdf(path: str):
    splitter = SentenceSplitter(chunk_size=1000, chunk_overlap=200)
    file_path = Path(path)
    docs = PDFReader().load_data(file=file_path)
    chunks = []

    for page_num, doc in enumerate(docs, start=1):
        if not getattr(doc, "text", None):
            continue

        page_chunks = splitter.split_text(doc.text)

        for i, chunk in enumerate(page_chunks):
            entry_id = str(
                uuid.uuid5(
                    uuid.NAMESPACE_URL,
                    f"{file_path.name}:{page_num}:{i}"
                )
            )

            chunks.append({
                "id": entry_id,
                "text": chunk,
                "page": page_num,
                "source": file_path.name
            })

    return chunks