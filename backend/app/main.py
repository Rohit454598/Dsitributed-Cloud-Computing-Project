from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.db import ensure_indexes
from app.routers import auth, evaluate, history, textbooks

settings = get_settings()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    try:
        ensure_indexes()
    except Exception as exc:  # noqa: BLE001
        # Allow boot without Mongo during first setup; routes will error clearly later.
        print(f"Warning: could not ensure MongoDB indexes: {exc}")
    yield


app = FastAPI(
    title="RAG Textbook Answer Evaluator",
    description="Upload textbooks, auto-build model answers with Gemini RAG, and evaluate student answers.",
    version="1.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list or ["*"],
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(textbooks.router)
app.include_router(evaluate.router)
app.include_router(history.router)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "TextbookGrade API is running. Open the app at http://127.0.0.1:5173",
        "docs": "http://127.0.0.1:8000/docs",
        "health": "http://127.0.0.1:8000/api/health",
    }


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
