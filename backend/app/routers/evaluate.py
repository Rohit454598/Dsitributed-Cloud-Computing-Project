from fastapi import APIRouter, Depends, HTTPException

from app.deps import CurrentUser, require_profile
from app.schemas import EvaluateRequest, EvaluateResponse
from app.services import evaluator, rag
from app.services import evaluations_store, textbook_meta

router = APIRouter(prefix="/api", tags=["evaluate"])


@router.post("/evaluate", response_model=EvaluateResponse)
def evaluate(
    payload: EvaluateRequest,
    user: CurrentUser = Depends(require_profile),
) -> EvaluateResponse:
    book = textbook_meta.assert_textbook_access(payload.textbook_id, user)

    try:
        sources = rag.retrieve_chunks(payload.textbook_id, payload.question)
        model_answer = rag.generate_model_answer(payload.question, sources)
        weights, feedback, score = evaluator.evaluate_answer_dynamic(
            question=payload.question,
            student_answer=payload.student_answer,
            model_answer=model_answer,
        )
        saved = evaluations_store.save_evaluation(
            user_id=user.uid,
            textbook_id=payload.textbook_id,
            textbook_owner_id=book["user_id"],
            textbook_filename=book.get("filename") or "",
            question=payload.question,
            student_answer=payload.student_answer,
            model_answer=model_answer,
            sources=sources,
            weights=weights,
            feedback=feedback,
            score=score,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        message = str(exc)
        status = 429 if "rate limit" in message.lower() else 500
        raise HTTPException(status_code=status, detail=message) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {exc}") from exc

    return EvaluateResponse(
        id=saved["id"],
        model_answer=model_answer,
        sources=sources,
        weights=weights,
        feedback=feedback,
        score=score,
    )
