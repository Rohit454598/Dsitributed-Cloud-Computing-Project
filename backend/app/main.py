from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import evaluate, textbooks

settings = get_settings()

app = FastAPI(
    title="RAG Textbook Answer Evaluator",
    description="Upload textbooks, auto-build model answers with Gemini RAG, and evaluate student answers.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list or ["*"],
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(textbooks.router)
app.include_router(evaluate.router)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
