from __future__ import annotations

import json
import re

from app.schemas import TraitWeights
from app.services.gemini_client import get_gemini


WEIGHTAGE_PROMPT = (
    "You are an expert evaluator. Analyze the given question and assign appropriate weightage "
    "(out of 100%) to the following grading traits:\n"
    "1. **Content Accuracy**: Importance of factual correctness and completeness.\n"
    "2. **Coherence & Structure**: Importance of logical flow and clarity.\n"
    "3. **Vocabulary & Clarity**: Importance of precise wording and expression.\n"
    "4. **Grammar & Language**: Importance of correct grammar and readability.\n\n"
    "Return ONLY a valid JSON object with these exact keys:\n"
    '{"content_accuracy": number, "coherence": number, "vocabulary": number, "grammar": number}\n'
    "The four numbers must sum to 100."
)


def assign_trait_weights(question: str) -> TraitWeights:
    gemini = get_gemini()
    raw = gemini.generate_text(
        system=WEIGHTAGE_PROMPT,
        user=f"Question: {question}",
        temperature=0.0,
    )

    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        raise ValueError(f"No valid JSON found in weight response: {raw}")

    weights = json.loads(match.group(0))
    required = {"content_accuracy", "coherence", "vocabulary", "grammar"}
    if not required.issubset(weights.keys()):
        raise ValueError(f"Invalid weight keys received: {weights}")

    total = sum(float(weights[k]) for k in required)
    if total <= 0:
        raise ValueError("Weight total must be positive.")

    normalized = {k: round((float(weights[k]) / total) * 100, 2) for k in required}
    return TraitWeights(**normalized)


def _extract_score(feedback: str) -> float | None:
    patterns = [
        r"[Oo]verall\s*[Ss]core[:\s]*([0-9]+(?:\.[0-9]+)?)\s*/\s*10",
        r"[Oo]verall\s*[Ss]core[:\s]*([0-9]+(?:\.[0-9]+)?)\s*/\s*100",
        r"\*\*[Oo]verall\s*[Ss]core[:\*]*\s*([0-9]+(?:\.[0-9]+)?)",
        r"([0-9]+(?:\.[0-9]+)?)\s*/\s*10",
    ]
    for pattern in patterns:
        match = re.search(pattern, feedback)
        if match:
            value = float(match.group(1))
            if "/100" in pattern or value > 10:
                return round(value / 10, 2)
            return round(value, 2)
    return None


def evaluate_answer_dynamic(
    question: str,
    student_answer: str,
    model_answer: str,
    weights: TraitWeights | None = None,
) -> tuple[TraitWeights, str, float | None]:
    weights = weights or assign_trait_weights(question)

    evaluation_prompt = (
        "You are an expert tutor giving improvement-only feedback.\n"
        "Compare the student's answer with the model answer using ONLY these traits:\n"
        f"1. **Content Accuracy ({weights.content_accuracy}%)**\n"
        f"2. **Coherence & Structure ({weights.coherence}%)**\n"
        f"3. **Vocabulary & Clarity ({weights.vocabulary}%)**\n"
        f"4. **Grammar & Language ({weights.grammar}%)**\n\n"
        "Rules for your response:\n"
        "- Do NOT rewrite a full model answer.\n"
        "- Do NOT give generic praise.\n"
        "- For EACH trait, include:\n"
        "  a) Mistakes / gaps found in the student's answer (quote short phrases when useful)\n"
        "  b) Exact improvements the student should make\n"
        "- If a trait has no mistakes, say 'No major issues' and give one refinement tip.\n"
        "- Keep the feedback practical and specific.\n"
        "- After the four traits, add a short 'Priority fixes' list (3 bullets max).\n"
        "- End with a weighted overall score out of 10 in this exact format: Overall Score: X/10"
    )

    user = (
        f"Question: {question}\n\n"
        f"Model Answer: {model_answer}\n\n"
        f"Student Answer: {student_answer}"
    )
    feedback = get_gemini().generate_text(
        system=evaluation_prompt,
        user=user,
        temperature=0.0,
    )
    score = _extract_score(feedback)
    return weights, feedback, score
