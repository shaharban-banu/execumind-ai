from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependencies import get_current_admin
from app.auth.schemas import (
    CreateUserRequest,
    UserManagementResponse,
)
from app.auth.security import hash_password
from database.database import SessionLocal
from database.models import User
from utils.logger import logger


router = APIRouter(
    prefix="/users",
    tags=["User Management"],
)


@router.post(
    "",
    response_model=UserManagementResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    request: CreateUserRequest,
    admin: User = Depends(get_current_admin),
):
    """
    Create an executive user.

    Only administrators can create users.
    """

    db = SessionLocal()

    try:
        existing_user = (
            db.query(User)
            .filter(User.username == request.username)
            .first()
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already exists.",
            )

        if request.email:
            existing_email = (
                db.query(User)
                .filter(User.email == request.email)
                .first()
            )

            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already exists.",
                )

        if len(request.password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least 8 characters.",
            )

        user = User(
            username=request.username,
            email=request.email,
            password_hash=hash_password(request.password),
            role="executive",
            is_active=True,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        logger.info(
            "Admin '%s' created user '%s'.",
            admin.username,
            user.username,
        )

        return user

    except HTTPException:
        db.rollback()
        raise

    except Exception:
        db.rollback()
        logger.exception("Failed to create user.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user.",
        )

    finally:
        db.close()


@router.get(
    "",
    response_model=list[UserManagementResponse],
)
def list_users(
    admin: User = Depends(get_current_admin),
):
    """
    List all users.

    Only administrators can access this endpoint.
    """

    db = SessionLocal()

    try:
        return (
            db.query(User)
            .order_by(User.id)
            .all()
        )

    finally:
        db.close()