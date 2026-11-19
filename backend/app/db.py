from __future__ import annotations

from functools import lru_cache

from pymongo import ASCENDING, DESCENDING, MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from app.config import get_settings


@lru_cache
def get_client() -> MongoClient:
    settings = get_settings()
    return MongoClient(settings.mongodb_uri)


def get_db() -> Database:
    settings = get_settings()
    return get_client()[settings.mongodb_db]


def users_col() -> Collection:
    return get_db()["users"]


def textbooks_col() -> Collection:
    return get_db()["textbooks"]


def evaluations_col() -> Collection:
    return get_db()["evaluations"]


def ensure_indexes() -> None:
    users_col().create_index("uid", unique=True)
    textbooks_col().create_index([("user_id", ASCENDING), ("created_at", DESCENDING)])
    textbooks_col().create_index("id", unique=True)
    evaluations_col().create_index([("user_id", ASCENDING), ("created_at", DESCENDING)])
    evaluations_col().create_index([("textbook_id", ASCENDING), ("created_at", DESCENDING)])
    evaluations_col().create_index("id", unique=True)
