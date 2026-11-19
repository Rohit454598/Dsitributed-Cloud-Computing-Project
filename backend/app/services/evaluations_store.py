from __future__ import annotations

import uuid
from datetime import datetime, timezone

from app.db import evaluations_col
from app.schemas import EvaluationRecord, SourceChunk, TraitWeights


def save_evaluation(
    *,
    user_id: str,
    textbook_id: str,
    textbook_owner_id: str,
    textbook_filename: str,
    question: str,
    student_answer: str,
    model_answer: str,
    sources: list[SourceChunk],
    weights: TraitWeights,
    feedback: str,
    score: float | None,
) -> dict:
    doc = {
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "textbook_id": textbook_id,
        "textbook_owner_id": textbook_owner_id,
        "textbook_filename": textbook_filename,
        "question": question,
        "student_answer": student_answer,
        "model_answer": model_answer,
        "sources": [s.model_dump() for s in sources],
        "weights": weights.model_dump(),
        "feedback": feedback,
        "score": score,
        "created_at": datetime.now(timezone.utc),
    }
    evaluations_col().insert_one(doc)
    return doc


def list_my_evaluations(user_id: str, limit: int = 50) -> list[EvaluationRecord]:
    docs = list(
        evaluations_col()
        .find({"user_id": user_id}, {"_id": 0})
        .sort("created_at", -1)
        .limit(limit)
    )
    return [EvaluationRecord(**doc) for doc in docs]


def list_textbook_evaluations(textbook_id: str, owner_id: str, limit: int = 50) -> list[EvaluationRecord]:
    docs = list(
        evaluations_col()
        .find(
            {"textbook_id": textbook_id, "textbook_owner_id": owner_id},
            {"_id": 0},
        )
        .sort("created_at", -1)
        .limit(limit)
    )
    return [EvaluationRecord(**doc) for doc in docs]
