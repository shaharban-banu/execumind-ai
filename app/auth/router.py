"""
Authentication API routes for ExecuMind AI.

Provides:
- Administrator login endpoint
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.auth.auth_service import AuthService
from app.auth.schemas import LoginRequest, TokenResponse
from utils.logger import logger

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post("/login",response_model=TokenResponse,
             status_code=status.HTTP_200_OK,
             summary="Administrator Login",
             description="authenticate administrator and return a JWT access token",)
def login(credentials:LoginRequest):
    """
    Authenticate administrator credentials.

    Args:
        credentials: Login request containing username and password.

    Returns:
        JWT access token.

    Raises:
        HTTPException:
            If authentication fails.
    """
    try:
        logger.info("Received login request for user '%s'",credentials.username,)
        response=AuthService.login(credentials)
        logger.info("Login request completed successfully for '%s'.",credentials.username,)
        return response

    except HTTPException:
        raise

    except Exception:
        logger.exception("Unexpected error occurred while processing login request.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        )
