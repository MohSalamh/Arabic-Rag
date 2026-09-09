from pathlib import Path
import uuid
import re

def save_uploaded_pdf(file) -> tuple[Path, str]:

    uploads_dir = Path("rag_uploads")

    uploads_dir.mkdir(parents=True, exist_ok=True)

    clean_name = re.sub(r"\s+","_", Path(file.name).name)

    file_path = (
        uploads_dir / f"{uuid.uuid4()}_{clean_name}"
    )

    file_bytes = file.getbuffer()
    file_path.write_bytes(file_bytes)

    return file_path, clean_name