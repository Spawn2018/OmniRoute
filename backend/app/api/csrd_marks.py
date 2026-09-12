from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.csrd_mark import CsrdMark
from app.services.csrd_marks.csrd_mark_service import CsrdMarkService

router = APIRouter(prefix="/csrd-marks", tags=["csrd"])

_PERM = "can_manage_csrd_marks"


class CsrdMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    report_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class CsrdMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    report_kind: str
    source_ref: str


def _row_out(row: CsrdMark) -> CsrdMarkResponse:
    return CsrdMarkResponse.model_validate(row)


@router.get("", response_model=list[CsrdMarkResponse])
async def list_csrd_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CsrdMarkResponse]:
    board = CsrdMarkService(session)
    return [_row_out(item) for item in await board.list_marks()]


@router.post("", response_model=CsrdMarkResponse, status_code=status.HTTP_201_CREATED)
async def create_csrd_mark(
    body: CsrdMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CsrdMarkResponse:
    board = CsrdMarkService(session)
    saved = await board.persist_csrd_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        report_kind=body.report_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "csrd-mark"
    return _row_out(saved)
