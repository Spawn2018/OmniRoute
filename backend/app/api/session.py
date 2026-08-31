from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity
from app.core.database import bind_tenant, get_session
from app.core.session_token import SessionIdentity
from app.services.tenancy.session_service import SessionService

router = APIRouter(prefix="/session", tags=["session"])


class SessionTokenRequest(BaseModel):
    organization_id: UUID
    user_id: UUID


class SessionTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class SessionMeResponse(BaseModel):
    user_id: UUID
    organization_id: UUID


@router.post("/token", response_model=SessionTokenResponse)
async def create_session_token(
    body: SessionTokenRequest,
    session: AsyncSession = Depends(get_session),
) -> SessionTokenResponse:
    await bind_tenant(session, body.organization_id)
    token = await SessionService(session).issue_for_app_user(
        organization_id=body.organization_id,
        user_id=body.user_id,
    )
    return SessionTokenResponse(access_token=token)


@router.get("/me", response_model=SessionMeResponse)
async def read_session(
    identity: SessionIdentity = Depends(get_current_identity),
) -> SessionMeResponse:
    return SessionMeResponse(
        user_id=identity.user_id,
        organization_id=identity.organization_id,
    )
