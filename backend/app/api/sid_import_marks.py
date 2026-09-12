from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.sid_import_mark import SidImportMark
from app.services.sid_import_marks.sid_import_mark_service import (
    SidImportMarkService,
)

router = APIRouter(prefix="/sid-import-marks", tags=["sid-import-marks"])

_PERM = "can_manage_sid_import_marks"


class SidImportMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    sid_kind: str
    source_ref: str


class SidImportMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    sid_kind: str
    source_ref: str


def _row(saved: SidImportMark) -> SidImportMarkResponse:
    return SidImportMarkResponse.model_validate(saved)


@router.get("", response_model=list[SidImportMarkResponse])
async def list_sid_import_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[SidImportMarkResponse]:
    packed = await SidImportMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=SidImportMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_sid_import_mark(
    body: SidImportMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> SidImportMarkResponse:
    saved = await SidImportMarkService(session).persist_sid_import_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        sid_kind=body.sid_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
