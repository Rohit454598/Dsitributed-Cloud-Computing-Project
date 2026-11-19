from pydantic import BaseModel, Field


class TextbookInfo(BaseModel):
    id: str
    filename: str
    chunk_count: int


class EvaluateRequest(BaseModel):
    textbook_id: str = Field(..., min_length=1)
    question: str = Field(..., min_length=1)
    student_answer: str = Field(..., min_length=1)


class TraitWeights(BaseModel):
    content_accuracy: float
    coherence: float
    vocabulary: float
    grammar: float


class SourceChunk(BaseModel):
    text: str
    score: float | None = None


class EvaluateResponse(BaseModel):
    model_answer: str
    sources: list[SourceChunk]
    weights: TraitWeights
    feedback: str
    score: float | None = None
