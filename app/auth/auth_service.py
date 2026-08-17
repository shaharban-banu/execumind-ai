"""
Provides authentication business logic for ExecuMind AI.

Responsibilities:
- Authenticate administrator
- Generate JWT access token
- Return authentication response
"""
from __future__ import annotations
from fastapi import HTTPException,status

from app.auth.schemas import LoginRequest,TokenResponse
from app.auth.security import authenticate_user,create_access_token
from utils.logger import logger

class AuthService:
    """
    Service class for administrator authentication.
    """
    @staticmethod
    def login(credentials:LoginRequest):
        """
        Authenticate administrator and generate JWT.

        Args:
            credentials: Administrator login credentials.

        Returns:
            JWT access token response.

        Raises:
            HTTPException:
                If authentication fails.
        """
        try:
            logger.info("Administrator login requested for user '%s'",credentials.username)
            user=authenticate_user(
                credentials.username,
                credentials.password,)
            if not user:
                logger.warning("Login failed for user '%s'",credentials.username)
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid username or password.",
                )
            access_token=create_access_token({
                "sub":str(user.id),
                "username":user.username,
                "role":user.role,
            })
            logger.info("Administrator '%s' logged in successfully",
                        credentials.username,)
            return TokenResponse(
                access_token=access_token,
                token_type="bearer",
                user={
                    "username": user.username,
                },
            )
        except HTTPException:
            raise
        except Exception:
            logger.exception("Unexpected error occured during administrator login")
            raise