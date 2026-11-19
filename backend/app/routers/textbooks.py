from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.config import get_settings
from app.deps import CurrentUser, require_profile
from app.schemas import TextbookInfo
from app.services import rag
from app.services import textbook_meta

router = APIRouter(prefix="/api/textbooks", tags=["textbooks"])


@router.get("", response_model=list[TextbookInfo])
def list_textbooks(user: CurrentUser = Depends(require_profile)) -> list[TextbookInfo]:
    docs = textbook_meta.list_visible_textbooks(user)
    return [
        TextbookInfo(
            id=doc["id"],
            filename=doc["filename"],
            chunk_count=doc.get("chunk_count", 0),
            user_id=doc.get("user_id"),
            owner_role=doc.get("owner_role") or doc.get("role"),
            shared=bool(doc.get("shared")),
            owned_by_me=bool(doc.get("owned_by_me")),
        )
        for doc in docs
    ]


@router.get("/quota")
def textbook_quota(user: CurrentUser = Depends(require_profile)) -> dict[str, int]:
    settings = get_settings()
    used = textbook_meta.count_user_textbooks(user.uid)
    return {
        "used": used,
        "max": settings.max_textbooks_per_user,
        "remaining": max(0, settings.max_textbooks_per_user - used),
    }


@router.post("", response_model=TextbookInfo)
async def upload_textbook(
    file: UploadFile = File(...),
    user: CurrentUser = Depends(require_profile),
) -> TextbookInfo:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required.")

    raw = await file.read()
    if not raw:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    # Enforce limit before expensive embedding work.
    settings = get_settings()
    if textbook_meta.count_user_textbooks(user.uid) >= settings.max_textbooks_per_user:
        raise HTTPException(
            status_code=400,
            detail=f"Textbook limit reached ({settings.max_textbooks_per_user}). Delete one to upload another.",
        )

    try:
        result = rag.index_textbook(file.filename, raw)
        meta = textbook_meta.create_textbook_meta(
            textbook_id=result["id"],
            user=user,
            filename=result["filename"],
            chunk_count=result["chunk_count"],
        )
    except HTTPException:
        raise
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        message = str(exc)
        status = 429 if "rate limit" in message.lower() else 500
        raise HTTPException(status_code=status, detail=message) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Upload failed: {exc}") from exc

    return TextbookInfo(
        id=result["id"],
        filename=result["filename"],
        chunk_count=result["chunk_count"],
        user_id=user.uid,
        owner_role=user.role,
        shared=bool(meta.get("shared")),
        owned_by_me=True,
    )


@router.delete("/{textbook_id}")
def delete_textbook(
    textbook_id: str,
    user: CurrentUser = Depends(require_profile),
) -> dict[str, str]:
    textbook_meta.delete_textbook_meta(textbook_id, user)
    try:
        rag.delete_textbook(textbook_id)
    except KeyError:
        # Meta removed; local vectors may already be gone.
        pass
    return {"status": "deleted", "id": textbook_id}
