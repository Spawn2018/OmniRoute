from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity
from app.core.database import get_session
from app.core.session_token import SessionIdentity
from app.services.tenancy.session_service import SessionService

router = APIRouter(prefix="/session", tags=["session"])


class SessionTokenRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=72)


class SessionRefreshRequest(BaseModel):
    refresh_token: str = Field(min_length=1, max_length=512)


class SessionTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class SessionMeResponse(BaseModel):
    user_id: UUID
    organization_id: UUID


@router.post("/token", response_model=SessionTokenResponse, status_code=status.HTTP_201_CREATED)
async def create_session_token(
    body: SessionTokenRequest,
    session: AsyncSession = Depends(get_session),
) -> SessionTokenResponse:
    issued = await SessionService(session).issue_for_credentials(
        email=str(body.email),
        password=body.password,
    )
    return SessionTokenResponse(
        access_token=issued.access_token,
        refresh_token=issued.refresh_token,
    )


@router.post("/refresh", response_model=SessionTokenResponse)
async def refresh_session(
    body: SessionRefreshRequest,
    session: AsyncSession = Depends(get_session),
) -> SessionTokenResponse:
    issued = await SessionService(session).rotate_refresh(body.refresh_token)
    return SessionTokenResponse(
        access_token=issued.access_token,
        refresh_token=issued.refresh_token,
    )


@router.get("/me", response_model=SessionMeResponse)
async def read_session(
    identity: SessionIdentity = Depends(get_current_identity),
) -> SessionMeResponse:
    return SessionMeResponse(
        user_id=identity.user_id,
        organization_id=identity.organization_id,
    )
