from __future__ import annotations

from datetime import datetime, timezone

from fastapi import HTTPException

from app.config import get_settings
from app.db import textbooks_col
from app.deps import CurrentUser


def count_user_textbooks(user_id: str) -> int:
    return textbooks_col().count_documents({"user_id": user_id})


def create_textbook_meta(
    *,
    textbook_id: str,
    user: CurrentUser,
    filename: str,
    chunk_count: int,
) -> dict:
    settings = get_settings()
    owned = count_user_textbooks(user.uid)
    if owned >= settings.max_textbooks_per_user:
        raise HTTPException(
            status_code=400,
            detail=f"Textbook limit reached ({settings.max_textbooks_per_user}). Delete one to upload another.",
        )

    shared = user.role == "teacher"
    doc = {
        "id": textbook_id,
        "user_id": user.uid,
        "role": user.role,
        "filename": filename,
        "chunk_count": chunk_count,
        "shared": shared,
        "created_at": datetime.now(timezone.utc),
    }
    textbooks_col().insert_one(doc)
    return doc


def delete_textbook_meta(textbook_id: str, user: CurrentUser) -> None:
    doc = textbooks_col().find_one({"id": textbook_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Textbook not found.")
    if doc.get("user_id") != user.uid:
        raise HTTPException(status_code=403, detail="You can only delete your own textbooks.")
    textbooks_col().delete_one({"id": textbook_id})


def get_textbook_meta(textbook_id: str) -> dict | None:
    return textbooks_col().find_one({"id": textbook_id}, {"_id": 0})


def list_visible_textbooks(user: CurrentUser) -> list[dict]:
    if user.role == "teacher":
        query = {"user_id": user.uid}
    else:
        query = {
            "$or": [
                {"user_id": user.uid},
                {"shared": True, "role": "teacher"},
            ]
        }

    docs = list(textbooks_col().find(query, {"_id": 0}).sort("created_at", -1))
    for doc in docs:
        doc["owned_by_me"] = doc.get("user_id") == user.uid
        doc["owner_role"] = doc.get("role")
    return docs


def assert_textbook_access(textbook_id: str, user: CurrentUser) -> dict:
    doc = get_textbook_meta(textbook_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Textbook not found.")

    owner = doc.get("user_id") == user.uid
    shared_teacher_book = bool(doc.get("shared")) and doc.get("role") == "teacher"
    if owner or shared_teacher_book:
        return doc
    raise HTTPException(status_code=403, detail="You do not have access to this textbook.")
