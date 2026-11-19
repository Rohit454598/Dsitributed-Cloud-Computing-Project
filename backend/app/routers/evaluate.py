from fastapi import APIRouter, HTTPException

from app.schemas import EvaluateRequest, EvaluateResponse
from app.services import evaluator, rag

router = APIRouter(prefix="/api", tags=["evaluate"])


@router.post("/evaluate", response_model=EvaluateResponse)
def evaluate(payload: EvaluateRequest) -> EvaluateResponse:
    try:
        sources = rag.retrieve_chunks(payload.textbook_id, payload.question)
        model_answer = rag.generate_model_answer(payload.question, sources)
        weights, feedback, score = evaluator.evaluate_answer_dynamic(
            question=payload.question,
            student_answer=payload.student_answer,
            model_answer=model_answer,
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
        model_answer=model_answer,
        sources=sources,
        weights=weights,
        feedback=feedback,
        score=score,
    )
