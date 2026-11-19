from fastapi import APIRouter, Depends

from app.deps import CurrentUser, get_current_user, require_profile, upsert_user_profile
from app.schemas import RegisterProfileRequest, UserProfile

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register-profile", response_model=UserProfile)
def register_profile(
    payload: RegisterProfileRequest,
    user: CurrentUser = Depends(get_current_user),
) -> UserProfile:
    doc = upsert_user_profile(
        uid=user.uid,
        email=user.email,
        role=payload.role,
        display_name=payload.display_name.strip(),
    )
    return UserProfile(
        uid=doc["uid"],
        email=doc.get("email") or user.email,
        role=doc["role"],
        display_name=doc.get("display_name") or "",
    )


@router.get("/me", response_model=UserProfile)
def me(user: CurrentUser = Depends(require_profile)) -> UserProfile:
    return UserProfile(
        uid=user.uid,
        email=user.email,
        role=user.role,
        display_name=user.display_name,
    )
