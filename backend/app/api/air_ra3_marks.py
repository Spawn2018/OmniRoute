from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.air_ra3_mark import AirRa3Mark
from app.services.air_ra3_marks.air_ra3_mark_service import AirRa3MarkService

router = APIRouter(prefix="/air-ra3-marks", tags=["air-ra3"])

_PERM = "can_manage_air_ra3_marks"


class AirRa3MarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    air_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class AirRa3MarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    air_kind: str
    source_ref: str


def _row_out(row: AirRa3Mark) -> AirRa3MarkResponse:
    return AirRa3MarkResponse.model_validate(row)


@router.get("", response_model=list[AirRa3MarkResponse])
async def list_air_ra3_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[AirRa3MarkResponse]:
    board = AirRa3MarkService(session)
    return [_row_out(item) for item in await board.list_marks()]


@router.post("", response_model=AirRa3MarkResponse, status_code=status.HTTP_201_CREATED)
async def create_air_ra3_mark(
    body: AirRa3MarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> AirRa3MarkResponse:
    board = AirRa3MarkService(session)
    saved = await board.persist_air_ra3_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        air_kind=body.air_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "air-ra3-mark"
    return _row_out(saved)
