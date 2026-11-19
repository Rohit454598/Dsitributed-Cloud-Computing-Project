from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

import firebase_admin
from firebase_admin import auth, credentials

from app.config import get_settings


@lru_cache
def init_firebase() -> firebase_admin.App:
    settings = get_settings()
    if firebase_admin._apps:
        return firebase_admin.get_app()

    if settings.firebase_credentials_json.strip():
        info = json.loads(settings.firebase_credentials_json)
        cred = credentials.Certificate(info)
    else:
        path = Path(settings.firebase_credentials_file)
        if not path.exists():
            raise RuntimeError(
                "Firebase credentials missing. Set FIREBASE_CREDENTIALS_JSON or place "
                "firebase-service-account.json in the backend folder."
            )
        cred = credentials.Certificate(str(path))

    options = {}
    if settings.firebase_project_id:
        options["projectId"] = settings.firebase_project_id
    return firebase_admin.initialize_app(cred, options or None)


def verify_id_token(token: str) -> dict:
    init_firebase()
    return auth.verify_id_token(token)
