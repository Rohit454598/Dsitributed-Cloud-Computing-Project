from datetime import datetime

from pydantic import BaseModel, Field


class TextbookInfo(BaseModel):
    id: str
    filename: str
    chunk_count: int
    user_id: str | None = None
    owner_role: str | None = None
    shared: bool = False
    owned_by_me: bool = False


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
    id: str | None = None
    model_answer: str
    sources: list[SourceChunk]
    weights: TraitWeights
    feedback: str
    score: float | None = None


class RegisterProfileRequest(BaseModel):
    role: str = Field(..., pattern="^(teacher|student)$")
    display_name: str = ""


class UserProfile(BaseModel):
    uid: str
    email: str
    role: str
    display_name: str = ""


class EvaluationRecord(BaseModel):
    id: str
    user_id: str
    textbook_id: str
    textbook_owner_id: str
    textbook_filename: str | None = None
    question: str
    student_answer: str
    model_answer: str
    sources: list[SourceChunk]
    weights: TraitWeights
    feedback: str
    score: float | None = None
    created_at: datetime | None = None
