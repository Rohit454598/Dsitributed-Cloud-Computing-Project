from __future__ import annotations

import re
import time

from google import genai
from google.genai import types
from google.genai.errors import APIError

from app.config import get_settings


class GeminiClient:
    def __init__(self) -> None:
        settings = get_settings()
        if not settings.gemini_api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is missing. Copy backend/.env.example to backend/.env and set your key."
            )
        self._settings = settings
        self._client = genai.Client(api_key=settings.gemini_api_key)

    def _retry_delay(self, exc: APIError) -> float:
        message = str(exc)
        match = re.search(r"retry in ([0-9]+(?:\.[0-9]+)?)s", message, re.I)
        if match:
            return min(float(match.group(1)) + 1.0, 90.0)
        return 20.0

    def _call_with_retry(self, fn, *, attempts: int = 6):
        last_error: Exception | None = None
        for attempt in range(attempts):
            try:
                return fn()
            except APIError as exc:
                last_error = exc
                code = getattr(exc, "status_code", None)
                text = str(exc)
                retryable = code in {429, 500, 503} or "RESOURCE_EXHAUSTED" in text or "UNAVAILABLE" in text
                if not retryable:
                    raise RuntimeError(self._friendly_error(exc)) from exc
                if attempt >= attempts - 1:
                    break
                delay = (
                    self._retry_delay(exc)
                    if code == 429 or "RESOURCE_EXHAUSTED" in text
                    else 2.5 * (attempt + 1)
                )
                time.sleep(delay)
        raise RuntimeError(
            "Gemini is busy or rate-limited. Wait about a minute and try again with a smaller PDF/TXT."
        ) from last_error

    def _friendly_error(self, exc: APIError) -> str:
        code = getattr(exc, "status_code", None)
        text = str(exc)
        if code == 401 or code == 403 or "API_KEY" in text.upper():
            return "Gemini API key is invalid or missing permissions. Check backend/.env."
        if code == 429 or "RESOURCE_EXHAUSTED" in text:
            return "Gemini rate limit exceeded. Wait about a minute and retry."
        if code == 404 or "NOT_FOUND" in text:
            return f"Gemini model not found. Update GEMINI_MODEL in backend/.env. Details: {text}"
        return f"Gemini API error: {text}"

    def generate_text(self, system: str, user: str, temperature: float = 0.0) -> str:
        def _run():
            # Gemini 3.x rejects legacy sampling params like temperature.
            config_kwargs: dict = {"system_instruction": system}
            model_name = self._settings.gemini_model.lower()
            if not model_name.startswith("gemini-3"):
                config_kwargs["temperature"] = temperature
            return self._client.models.generate_content(
                model=self._settings.gemini_model,
                contents=user,
                config=types.GenerateContentConfig(**config_kwargs),
            )

        response = self._call_with_retry(_run)
        text = (response.text or "").strip()
        if not text:
            raise RuntimeError("Gemini returned an empty response.")
        return text

    def embed_texts(self, texts: list[str], task_type: str = "RETRIEVAL_DOCUMENT") -> list[list[float]]:
        if not texts:
            return []

        # Free-tier embed RPM is low; keep batches small and pace requests.
        embeddings: list[list[float]] = []
        batch_size = 16
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]

            def _run(current_batch=batch):
                return self._client.models.embed_content(
                    model=self._settings.gemini_embedding_model,
                    contents=current_batch,
                    config=types.EmbedContentConfig(task_type=task_type),
                )

            result = self._call_with_retry(_run)
            if not result.embeddings:
                raise RuntimeError("Gemini embedding call returned no vectors.")
            for item in result.embeddings:
                if not item.values:
                    raise RuntimeError("Gemini returned an empty embedding vector.")
                embeddings.append(list(item.values))

            if i + batch_size < len(texts):
                time.sleep(1.2)

        return embeddings

    def embed_query(self, text: str) -> list[float]:
        vectors = self.embed_texts([text], task_type="RETRIEVAL_QUERY")
        return vectors[0]


_client: GeminiClient | None = None


def get_gemini() -> GeminiClient:
    global _client
    if _client is None:
        _client = GeminiClient()
    return _client
