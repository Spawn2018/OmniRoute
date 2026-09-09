from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.local_charge import LocalCharge
from app.services.local_charges.local_charge_service import LocalChargeService

router = APIRouter(prefix="/local-charges", tags=["local-charges"])

_PERM = "can_manage_local_charges"


class LocalChargeCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    charge_kind: str
    amount: str
    currency: str
    source_ref: str
    port_unlocode: str | None = None


class LocalChargeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    charge_kind: str
    amount: str
    currency: str
    port_unlocode: str | None
    source_ref: str


def _as_row(row: LocalCharge) -> LocalChargeResponse:
    return LocalChargeResponse(
        id=row.id,
        organization_id=row.organization_id,
        charge_kind=row.charge_kind,
        amount=format(row.amount, "f"),
        currency=str(row.currency).strip(),
        port_unlocode=row.port_unlocode,
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[LocalChargeResponse])
async def list_local_charges(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[LocalChargeResponse]:
    rows = await LocalChargeService(session).list_levies()
    return [_as_row(row) for row in rows]


@router.post("", response_model=LocalChargeResponse, status_code=status.HTTP_201_CREATED)
async def create_local_charge(
    body: LocalChargeCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> LocalChargeResponse:
    row = await LocalChargeService(session).record_levy(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        charge_kind=body.charge_kind,
        amount=body.amount,
        currency=body.currency,
        source_ref=body.source_ref,
        port_unlocode=body.port_unlocode,
    )
    await session.commit()
    return _as_row(row)
