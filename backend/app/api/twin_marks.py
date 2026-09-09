from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.twin_mark import TwinMark
from app.services.twin_marks.twin_mark_service import TwinMarkService

router = APIRouter(prefix="/twin-marks", tags=["twin-marks"])

_PERM = "can_manage_twin_marks"


class TwinMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    twin_kind: str
    source_ref: str


class TwinMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    twin_kind: str
    source_ref: str


def _as_row(row: TwinMark) -> TwinMarkResponse:
    return TwinMarkResponse.model_validate(row)


@router.get("", response_model=list[TwinMarkResponse])
async def list_twin_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[TwinMarkResponse]:
    rows = await TwinMarkService(session).list_marks()
    return [_as_row(row) for row in rows]


@router.post("", response_model=TwinMarkResponse, status_code=status.HTTP_201_CREATED)
async def create_twin_mark(
    body: TwinMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TwinMarkResponse:
    row = await TwinMarkService(session).persist_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        twin_kind=body.twin_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
