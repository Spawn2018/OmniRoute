from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.executive_mark import ExecutiveMark
from app.services.executive_marks.executive_mark_service import ExecutiveMarkService

router = APIRouter(prefix="/executive-marks", tags=["executive-marks"])

_PERM = "can_manage_executive_marks"


class ExecutiveMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question_kind: str
    source_ref: str


class ExecutiveMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    question_kind: str
    source_ref: str


def _as_row(row: ExecutiveMark) -> ExecutiveMarkResponse:
    return ExecutiveMarkResponse.model_validate(row)


@router.get("", response_model=list[ExecutiveMarkResponse])
async def list_executive_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ExecutiveMarkResponse]:
    rows = await ExecutiveMarkService(session).list_briefs()
    return [_as_row(row) for row in rows]


@router.post("", response_model=ExecutiveMarkResponse, status_code=status.HTTP_201_CREATED)
async def create_executive_mark(
    body: ExecutiveMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ExecutiveMarkResponse:
    row = await ExecutiveMarkService(session).record_brief(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        question_kind=body.question_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
