"""Authentication middleware for FastAPI."""
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from jose import jwt, JWTError
import os


security = HTTPBearer()


def create_access_token(data: dict) -> str:
    """Create JWT access token.
    
    Args:
        data: Data to encode in token
        
    Returns:
        Encoded JWT token
    """
    secret_key = os.getenv("SECRET_KEY", "change-this-secret-key")
    return jwt.encode(data, secret_key, algorithm="HS256")


def verify_token(token: str) -> dict:
    """Verify and decode JWT token.
    
    Args:
        token: JWT token to verify
        
    Returns:
        Decoded token data
        
    Raises:
        HTTPException: If token is invalid
    """
    try:
        secret_key = os.getenv("SECRET_KEY", "change-this-secret-key")
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> dict:
    """Dependency to get current authenticated user.
    
    Args:
        credentials: HTTP Bearer credentials
        
    Returns:
        Current user data from token
        
    Raises:
        HTTPException: If authentication fails
    """
    token = credentials.credentials
    return verify_token(token)


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security)
) -> Optional[dict]:
    """Dependency to get current user if authenticated, None otherwise.
    
    Args:
        credentials: HTTP Bearer credentials
        
    Returns:
        Current user data or None
    """
    if credentials:
        try:
            return verify_token(credentials.credentials)
        except HTTPException:
            return None
    return None
