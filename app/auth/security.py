"""
Provides authentication utilities for ExecuMind AI.

Responsibilities:
- Authenticate administrator credentials
- Generate JWT access tokens
- Verify JWT access tokens
"""
from __future__ import annotations
from datetime import datetime,timedelta,timezone
import os
from dotenv import load_dotenv
from fastapi import HTTPException
from jose import jwt,JWTError,ExpiredSignatureError
from passlib.context import CryptContext
from utils.logger import logger

load_dotenv()

ADMIN_USERNAME=os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD_HASH=os.getenv("ADMIN_PASSWORD")

JWT_SECRET=os.getenv("JWT_SECRET")
JWT_ALGORITHM=os.getenv("JWT_ALGORITHM","HS256")
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES",30))

#password hashing
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password:str):
    """
    Hash a plain-text password using bcrypt.

    Args:
        password: Plain-text password.

    Returns:
        Bcrypt hashed password.

    Raises:
        Exception: If hashing fails.
    """
    try:
        logger.info("Hashing administrator password")
        password=password.encode("utf-8")[:72].decode("utf-8","ignore")
        return pwd_context.hash(password)
    except Exception:
        logger.exception("Failed to hash password")
        raise

def verify_password(plain_password:str,hashed_password:str):
    """
    Verify a password against its bcrypt hash.

    Args:
        plain_password: User entered password.
        hashed_password: Stored bcrypt hash.

    Returns:
        True if password matches, otherwise False.
    """
    try:
        plain_password = plain_password.encode("utf-8")[:72].decode("utf-8", "ignore")
        return pwd_context.verify(plain_password,hashed_password)
    except Exception:
        logger.exception("password verification failed")
        raise

def authenticate_user(username:str,password:str):
    """
    Authenticate administrator credentials.

    Args:
        username: Login username.
        password: Login password.

    Returns:
        True if authentication succeeds,
        otherwise False.
    """
    try:
        logger.info("Authentication attempt for user '%s'",username,)

        if username!=ADMIN_USERNAME:
            logger.warning("Authentication failed.Invalid username")
            return False
        if not verify_password(password,ADMIN_PASSWORD_HASH,):
            logger.warning("Authentication failed.Invalid password")
            return False
        logger.info("Administtrator authenticated succeessfully")
        return True
    except Exception:
        logger.exception("Unexpectd error during authentication")
        raise


def create_access_token(data:dict):
    """
    Generate a signed JWT access token.

    Args:
        data: Payload to encode into the JWT.

    Returns:
        Encoded JWT access token.
    """
    try:
        to_encode=data.copy()
        expire=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp":expire})

        logger.info("JWT access token created successfully.")
        token= jwt.encode(to_encode,JWT_SECRET,algorithm=JWT_ALGORITHM,)
        logger.info("JWT access token created successfully.")

        return token
    except Exception:
        logger.exception("Failed to create JWT access token")
        raise

def verify_token(token:str):
    """
    Verify and decode a JWT access token.

    Args:
        token: JWT access token.

    Returns:
        Decoded payload if valid,
        otherwise None.
    """
    try:
        payload=jwt.decode(token,JWT_SECRET,algorithms=[JWT_ALGORITHM],)
        logger.info("JWT token verified successfully.")
        return payload
    except ExpiredSignatureError:
        logger.warning("JWT token has expired.")

        raise HTTPException(
            status_code=401,
            detail="Token has expired.",
        )

    except JWTError:
        logger.warning("Invalid JWT token.")

        raise HTTPException(
            status_code=401,
        detail="Invalid authentication credentials.",
    )