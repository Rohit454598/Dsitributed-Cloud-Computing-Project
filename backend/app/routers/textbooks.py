from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas import TextbookInfo
from app.services import rag

router = APIRouter(prefix="/api/textbooks", tags=["textbooks"])


@router.get("", response_model=list[TextbookInfo])
def list_textbooks() -> list[TextbookInfo]:
    return [TextbookInfo(**item) for item in rag.list_textbooks()]


@router.post("", response_model=TextbookInfo)
async def upload_textbook(file: UploadFile = File(...)) -> TextbookInfo:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required.")

    raw = await file.read()
    if not raw:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        result = rag.index_textbook(file.filename, raw)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        message = str(exc)
        status = 429 if "rate limit" in message.lower() else 500
        raise HTTPException(status_code=status, detail=message) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Upload failed: {exc}") from exc

    return TextbookInfo(**result)


@router.delete("/{textbook_id}")
def delete_textbook(textbook_id: str) -> dict[str, str]:
    try:
        rag.delete_textbook(textbook_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"status": "deleted", "id": textbook_id}
