from fastapi import APIRouter, Depends, HTTPException

from app.deps import CurrentUser, require_profile
from app.schemas import EvaluationRecord
from app.services import evaluations_store, textbook_meta

router = APIRouter(prefix="/api/evaluations", tags=["evaluations"])


@router.get("/me", response_model=list[EvaluationRecord])
def my_evaluations(user: CurrentUser = Depends(require_profile)) -> list[EvaluationRecord]:
    return evaluations_store.list_my_evaluations(user.uid)


@router.get("/textbook/{textbook_id}", response_model=list[EvaluationRecord])
def textbook_evaluations(
    textbook_id: str,
    user: CurrentUser = Depends(require_profile),
) -> list[EvaluationRecord]:
    if user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can view textbook evaluation feeds.")

    book = textbook_meta.get_textbook_meta(textbook_id)
    if not book:
        raise HTTPException(status_code=404, detail="Textbook not found.")
    if book.get("user_id") != user.uid:
        raise HTTPException(status_code=403, detail="You can only view evaluations for your own textbooks.")

    return evaluations_store.list_textbook_evaluations(textbook_id, user.uid)
