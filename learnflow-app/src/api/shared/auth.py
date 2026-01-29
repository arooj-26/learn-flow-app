"""Authentication middleware for FastAPI agents.

Provides token verification and user extraction for protected endpoints.
Works with Better Auth session tokens passed as Bearer tokens.
"""
import os
from functools import wraps
from typing import Optional
from uuid import UUID

import httpx
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

# Security scheme for Bearer token
security = HTTPBearer(auto_error=False)

# Better Auth server URL (Next.js app)
BETTER_AUTH_URL = os.getenv("BETTER_AUTH_URL", "http://localhost:3000")


class AuthenticatedUser(BaseModel):
    """Represents an authenticated user from the session."""
    id: UUID
    email: str
    name: str
    role: str = "student"
    image: Optional[str] = None
    email_verified: bool = False


async def verify_token(token: str) -> Optional[AuthenticatedUser]:
    """Verify a Bearer token with the Better Auth server.

    Makes a request to the Better Auth session endpoint to validate
    the token and retrieve user information.

    Args:
        token: The Bearer token to verify

    Returns:
        AuthenticatedUser if valid, None if invalid
    """
    try:
        async with httpx.AsyncClient() as client:
            # Call Better Auth's session endpoint
            response = await client.get(
                f"{BETTER_AUTH_URL}/api/auth/session",
                headers={"Authorization": f"Bearer {token}"},
                cookies={"better-auth.session_token": token},
                timeout=10.0,
            )

            if response.status_code != 200:
                return None

            data = response.json()
            if not data or "user" not in data:
                return None

            user_data = data["user"]
            return AuthenticatedUser(
                id=UUID(user_data["id"]),
                email=user_data["email"],
                name=user_data["name"],
                role=user_data.get("role", "student"),
                image=user_data.get("image"),
                email_verified=user_data.get("emailVerified", False),
            )
    except Exception:
        return None


async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> AuthenticatedUser:
    """FastAPI dependency to get the current authenticated user.

    Extracts the Bearer token from the Authorization header and verifies it.
    Raises 401 if no token or invalid token.

    Usage:
        @app.get("/protected")
        async def protected_route(user: AuthenticatedUser = Depends(get_current_user)):
            return {"user_id": str(user.id)}
    """
    # Try Bearer token first
    token = None
    if credentials:
        token = credentials.credentials

    # Fall back to cookie if no Bearer token
    if not token:
        token = request.cookies.get("better-auth.session_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await verify_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_user_optional(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> Optional[AuthenticatedUser]:
    """FastAPI dependency to optionally get the current user.

    Returns None if not authenticated instead of raising an exception.

    Usage:
        @app.get("/public")
        async def public_route(user: Optional[AuthenticatedUser] = Depends(get_current_user_optional)):
            if user:
                return {"message": f"Hello {user.name}"}
            return {"message": "Hello guest"}
    """
    token = None
    if credentials:
        token = credentials.credentials

    if not token:
        token = request.cookies.get("better-auth.session_token")

    if not token:
        return None

    return await verify_token(token)


def require_role(required_role: str):
    """Dependency factory to require a specific role.

    Usage:
        @app.get("/teacher-only")
        async def teacher_route(user: AuthenticatedUser = Depends(require_role("teacher"))):
            return {"message": "Teacher access granted"}
    """
    async def role_checker(user: AuthenticatedUser = Depends(get_current_user)) -> AuthenticatedUser:
        if user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role: {required_role}",
            )
        return user

    return role_checker


# Convenience dependencies
require_student = require_role("student")
require_teacher = require_role("teacher")


def extract_student_id(user: AuthenticatedUser = Depends(get_current_user)) -> UUID:
    """Extract just the student ID from the authenticated user.

    Convenience dependency for endpoints that only need the user ID.

    Usage:
        @app.post("/submit")
        async def submit_code(student_id: UUID = Depends(extract_student_id), code: str):
            # student_id is extracted from auth token
            ...
    """
    return user.id
