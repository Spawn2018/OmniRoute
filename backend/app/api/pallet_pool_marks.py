from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.pallet_pool_mark import PalletPoolMark
from app.services.pallet_pool_marks.pallet_pool_mark_service import (
    PalletPoolMarkService,
)

router = APIRouter(prefix="/pallet-pool-marks", tags=["pallet-pool-marks"])

_PERM = "can_manage_pallet_pool_marks"


class PalletPoolMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    pool_kind: str
    source_ref: str


class PalletPoolMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    pool_kind: str
    source_ref: str


def _row(saved: PalletPoolMark) -> PalletPoolMarkResponse:
    return PalletPoolMarkResponse.model_validate(saved)


@router.get("", response_model=list[PalletPoolMarkResponse])
async def list_pallet_pool_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[PalletPoolMarkResponse]:
    packed = await PalletPoolMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=PalletPoolMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_pallet_pool_mark(
    body: PalletPoolMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> PalletPoolMarkResponse:
    saved = await PalletPoolMarkService(session).persist_pallet_pool_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        pool_kind=body.pool_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
