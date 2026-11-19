from __future__ import annotations

import re
import uuid
from pathlib import Path

from pypdf import PdfReader

from app.config import get_settings
from app.schemas import SourceChunk
from app.services import vector_store
from app.services.gemini_client import get_gemini


def _extract_text(file_path: Path) -> str:
    suffix = file_path.suffix.lower()
    if suffix == ".txt":
        return file_path.read_text(encoding="utf-8", errors="ignore")
    if suffix == ".pdf":
        reader = PdfReader(str(file_path))
        pages = []
        for page in reader.pages:
            pages.append(page.extract_text() or "")
        return "\n".join(pages)
    raise ValueError("Only PDF and TXT files are supported.")


def _chunk_text(text: str, chunk_size: int, overlap: int, max_chunks: int = 60) -> list[str]:
    cleaned = re.sub(r"\s+", " ", text).strip()
    if not cleaned:
        return []
    chunks: list[str] = []
    start = 0
    length = len(cleaned)
    while start < length and len(chunks) < max_chunks:
        end = min(start + chunk_size, length)
        chunk = cleaned[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= length:
            break
        start = max(0, end - overlap)
    return chunks


def list_textbooks() -> list[dict]:
    meta = vector_store.load_metadata()
    return [
        {
            "id": book_id,
            "filename": info["filename"],
            "chunk_count": info["chunk_count"],
        }
        for book_id, info in meta.items()
    ]


def index_textbook(filename: str, raw_bytes: bytes) -> dict:
    settings = get_settings()
    suffix = Path(filename).suffix.lower()
    if suffix not in {".pdf", ".txt"}:
        raise ValueError("Only PDF and TXT files are supported.")

    textbook_id = str(uuid.uuid4())
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    saved_path = upload_dir / f"{textbook_id}{suffix}"
    saved_path.write_bytes(raw_bytes)

    text = _extract_text(saved_path)
    chunks = _chunk_text(text, settings.chunk_size, settings.chunk_overlap)
    if not chunks:
        saved_path.unlink(missing_ok=True)
        raise ValueError(
            "No readable text found in the uploaded file. "
            "Use a text-based PDF or TXT (scanned image PDFs are not supported)."
        )

    gemini = get_gemini()
    embeddings = gemini.embed_texts(chunks, task_type="RETRIEVAL_DOCUMENT")
    vector_store.save_book_vectors(textbook_id, chunks, embeddings)

    meta = vector_store.load_metadata()
    meta[textbook_id] = {
        "filename": filename,
        "chunk_count": len(chunks),
        "path": str(saved_path),
    }
    vector_store.save_metadata(meta)

    return {
        "id": textbook_id,
        "filename": filename,
        "chunk_count": len(chunks),
    }


def delete_textbook(textbook_id: str) -> None:
    meta = vector_store.load_metadata()
    if textbook_id not in meta:
        raise KeyError("Textbook not found.")

    info = meta.pop(textbook_id)
    vector_store.save_metadata(meta)
    vector_store.delete_book_vectors(textbook_id)

    path = Path(info.get("path", ""))
    if path.exists():
        path.unlink()


def retrieve_chunks(textbook_id: str, question: str, top_k: int | None = None) -> list[SourceChunk]:
    meta = vector_store.load_metadata()
    if textbook_id not in meta:
        raise KeyError("Textbook not found.")

    settings = get_settings()
    k = top_k or settings.top_k
    query_embedding = get_gemini().embed_query(question)
    hits = vector_store.query_book(textbook_id, query_embedding, k)
    return [
        SourceChunk(text=text, score=round(score, 4))
        for text, score in hits
    ]


def generate_model_answer(question: str, sources: list[SourceChunk]) -> str:
    if not sources:
        raise ValueError("No textbook context found for this question.")

    context_blocks = []
    for i, source in enumerate(sources, start=1):
        context_blocks.append(f"[Source {i}]\n{source.text}")
    context = "\n\n".join(context_blocks)

    system = (
        "You are a subject-matter expert writing a model answer for student assessment. "
        "Use ONLY the provided textbook excerpts. Do not invent facts that are not supported "
        "by the sources. Write a clear, complete answer suitable as a grading reference. "
        "If the sources are insufficient, say what is missing briefly and answer only from what is available."
    )
    user = f"Question:\n{question}\n\nTextbook excerpts:\n{context}\n\nWrite the model answer:"
    return get_gemini().generate_text(system=system, user=user, temperature=0.2)
