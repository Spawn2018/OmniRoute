from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.services.fraud_flags.fraud_flag_service import FraudFlagService
from app.services.parties.party_service import PartyService

router = APIRouter(prefix="/fraud-flags", tags=["fraud-flags"])


class FraudFlagCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    party_id: UUID
    flag_kind: str
    source_ref: str


class FraudFlagResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    party_id: UUID
    flag_kind: str
    source_ref: str


@router.get("", response_model=list[FraudFlagResponse])
async def list_fraud_flags(
    _authz: None = Depends(require_permission("can_manage_fraud_flags", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[FraudFlagResponse]:
    rows = await FraudFlagService(session).list_flags()
    return [FraudFlagResponse.model_validate(row) for row in rows]


@router.post("", response_model=FraudFlagResponse, status_code=status.HTTP_201_CREATED)
async def create_fraud_flag(
    body: FraudFlagCreate,
    _authz: None = Depends(require_permission("can_manage_fraud_flags", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> FraudFlagResponse:
    party = await PartyService(session).get_party(body.party_id)
    row = await FraudFlagService(session).record_flag(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        party_id=party.id,
        flag_kind=body.flag_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return FraudFlagResponse.model_validate(row)
