from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from fastapi import Depends, Header, HTTPException

from app.db import users_col
from app.services.firebase_auth import verify_id_token


@dataclass
class CurrentUser:
    uid: str
    email: str
    role: str
    display_name: str


def _bearer_token(authorization: str | None) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header.")
    parts = authorization.split(" ", 1)
    if len(parts) != 2 or parts[0].lower() != "bearer" or not parts[1].strip():
        raise HTTPException(status_code=401, detail="Invalid Authorization header.")
    return parts[1].strip()


def get_current_user(authorization: str | None = Header(default=None)) -> CurrentUser:
    token = _bearer_token(authorization)
    try:
        decoded = verify_id_token(token)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=401, detail=f"Invalid Firebase token: {exc}") from exc

    uid = decoded.get("uid") or decoded.get("sub")
    if not uid:
        raise HTTPException(status_code=401, detail="Token missing uid.")

    email = decoded.get("email") or ""
    profile = users_col().find_one({"uid": uid})
    if not profile:
        # Allow authenticated calls that only need identity before profile creation.
        return CurrentUser(uid=uid, email=email, role="", display_name="")

    return CurrentUser(
        uid=uid,
        email=profile.get("email") or email,
        role=profile.get("role") or "",
        display_name=profile.get("display_name") or "",
    )


def require_profile(user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    if user.role not in {"teacher", "student"}:
        raise HTTPException(
            status_code=403,
            detail="Complete signup profile first (POST /api/auth/register-profile).",
        )
    return user


def upsert_user_profile(
    *,
    uid: str,
    email: str,
    role: str,
    display_name: str = "",
) -> dict:
    if role not in {"teacher", "student"}:
        raise HTTPException(status_code=400, detail="Role must be 'teacher' or 'student'.")

    now = datetime.now(timezone.utc)
    existing = users_col().find_one({"uid": uid})
    if existing:
        users_col().update_one(
            {"uid": uid},
            {
                "$set": {
                    "email": email or existing.get("email", ""),
                    "display_name": display_name or existing.get("display_name", ""),
                    "updated_at": now,
                }
            },
        )
        doc = users_col().find_one({"uid": uid})
        assert doc is not None
        return doc

    doc = {
        "uid": uid,
        "email": email,
        "role": role,
        "display_name": display_name,
        "created_at": now,
        "updated_at": now,
    }
    users_col().insert_one(doc)
    return doc
