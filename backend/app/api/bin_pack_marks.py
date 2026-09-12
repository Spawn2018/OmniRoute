from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.bin_pack_mark import BinPackMark
from app.services.bin_pack_marks.bin_pack_mark_service import (
    BinPackMarkService,
)

router = APIRouter(prefix="/bin-pack-marks", tags=["bin-pack-marks"])

_PERM = "can_manage_bin_pack_marks"


class BinPackMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    pack_kind: str
    source_ref: str


class BinPackMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    pack_kind: str
    source_ref: str


def _row(saved: BinPackMark) -> BinPackMarkResponse:
    return BinPackMarkResponse.model_validate(saved)


@router.get("", response_model=list[BinPackMarkResponse])
async def list_bin_pack_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[BinPackMarkResponse]:
    packed = await BinPackMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=BinPackMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_bin_pack_mark(
    body: BinPackMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> BinPackMarkResponse:
    saved = await BinPackMarkService(session).persist_bin_pack_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        pack_kind=body.pack_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
