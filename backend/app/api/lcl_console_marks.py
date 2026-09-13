from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.lcl_console_mark import LclConsoleMark
from app.services.lcl_console_marks.lcl_console_mark_service import LclConsoleMarkService

router = APIRouter(prefix="/lcl-console-marks", tags=["lcl-console-marks"])

_PERM = "can_manage_lcl_console_marks"


class LclConsoleMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    console_kind: str
    source_ref: str


class LclConsoleMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    console_kind: str
    source_ref: str


def _row(saved: LclConsoleMark) -> LclConsoleMarkResponse:
    return LclConsoleMarkResponse.model_validate(saved)


@router.get("", response_model=list[LclConsoleMarkResponse])
async def list_lcl_console_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[LclConsoleMarkResponse]:
    packed = await LclConsoleMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=LclConsoleMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_lcl_console_mark(
    body: LclConsoleMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> LclConsoleMarkResponse:
    saved = await LclConsoleMarkService(session).persist_lcl_console_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        console_kind=body.console_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
