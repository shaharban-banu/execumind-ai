"""
Authentication dependencies for ExecuMind AI.

Responsibilities:
- Extract JWT token from Authorization header
- Verify JWT token
- Return authenticated administrator
"""
from __future__ import annotations

from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from database.database import SessionLocal
from database.models import User
from app.auth.security import verify_token
from utils.logger import logger

security=HTTPBearer()

def get_current_user(credentials:HTTPAuthorizationCredentials=Depends(security)):
    """
    Validate JWT token and return authenticated database user.
    """

    db=SessionLocal()

    try:
        token=credentials.credentials
        logger.info("Verifying JWT access token.")

        payload = verify_token(token)

        if payload is None:
            logger.warning("Invalid or expired JWT.")

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired authentication token.",
            )
        user_id=payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
            )

        user=(db.query(User).filter(User.id==int(user_id)).first())
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User no longer exists"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive.",
            )

        logger.info(
            "Authenticated user '%s' (id=%s, role=%s).",
            user.username,user.id,user.role,
        )

        return user

    except HTTPException:
        raise

    except Exception:
        logger.exception(
            "Unexpected authentication dependency error."
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication failed.",
        )

    finally:
        db.close()

def get_current_admin(
    user: User = Depends(get_current_user),
):
    """
    Allow access only to administrator users.
    """

    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required.",
        )

    return user