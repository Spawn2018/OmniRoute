from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.bonded_mark import BondedMark
from app.services.bonded_marks.bonded_mark_service import BondedMarkService

router = APIRouter(prefix="/bonded-marks", tags=["bonded-marks"])

_PERM = "can_manage_bonded_marks"


class BondedMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    bond_kind: str
    source_ref: str


class BondedMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    bond_kind: str
    source_ref: str


def _row(saved: BondedMark) -> BondedMarkResponse:
    return BondedMarkResponse.model_validate(saved)


@router.get("", response_model=list[BondedMarkResponse])
async def list_bonded_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[BondedMarkResponse]:
    packed = await BondedMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=BondedMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_bonded_mark(
    body: BondedMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> BondedMarkResponse:
    saved = await BondedMarkService(session).persist_bonded_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        bond_kind=body.bond_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
