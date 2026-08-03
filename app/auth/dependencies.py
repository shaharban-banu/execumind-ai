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

from app.auth.security import verify_token
from utils.logger import logger

security=HTTPBearer()

def get_current_user(credentials:HTTPAuthorizationCredentials=Depends(security)):
    """
    Validate JWT token and return authenticated user.

    Args:
        credentials: HTTP Bearer credentials.

    Returns:
        Decoded JWT payload.

    Raises:
        HTTPException:
            If token is invalid or expired.
    """
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

        logger.info(
            "Authenticated user '%s'.",
            payload.get("sub"),
        )

        return payload

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