from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from app.config import get_settings


def _store_dir() -> Path:
    path = Path(get_settings().chroma_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def _meta_path() -> Path:
    return _store_dir() / "textbooks.json"


def _book_dir(textbook_id: str) -> Path:
    return _store_dir() / textbook_id


def load_metadata() -> dict[str, dict]:
    path = _meta_path()
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_metadata(data: dict[str, dict]) -> None:
    _meta_path().write_text(json.dumps(data, indent=2), encoding="utf-8")


def save_book_vectors(
    textbook_id: str,
    chunks: list[str],
    embeddings: list[list[float]],
) -> None:
    book_path = _book_dir(textbook_id)
    book_path.mkdir(parents=True, exist_ok=True)
    (book_path / "chunks.json").write_text(
        json.dumps(chunks, ensure_ascii=False),
        encoding="utf-8",
    )
    np.save(book_path / "embeddings.npy", np.asarray(embeddings, dtype=np.float32))


def delete_book_vectors(textbook_id: str) -> None:
    book_path = _book_dir(textbook_id)
    if not book_path.exists():
        return
    for child in book_path.iterdir():
        child.unlink()
    book_path.rmdir()


def query_book(
    textbook_id: str,
    query_embedding: list[float],
    top_k: int,
) -> list[tuple[str, float]]:
    book_path = _book_dir(textbook_id)
    chunks_path = book_path / "chunks.json"
    emb_path = book_path / "embeddings.npy"
    if not chunks_path.exists() or not emb_path.exists():
        raise KeyError("Textbook vectors not found.")

    chunks: list[str] = json.loads(chunks_path.read_text(encoding="utf-8"))
    matrix = np.load(emb_path)
    if matrix.size == 0:
        return []

    query = np.asarray(query_embedding, dtype=np.float32)
    query_norm = np.linalg.norm(query) + 1e-12
    doc_norms = np.linalg.norm(matrix, axis=1) + 1e-12
    scores = (matrix @ query) / (doc_norms * query_norm)

    k = min(top_k, len(chunks))
    top_idx = np.argsort(-scores)[:k]
    return [(chunks[int(i)], float(scores[int(i)])) for i in top_idx]
