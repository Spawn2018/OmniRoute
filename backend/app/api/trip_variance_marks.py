from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.trip_variance_mark import TripVarianceMark
from app.services.trip_variance_marks.trip_variance_mark_service import (
    TripVarianceMarkService,
)

router = APIRouter(
    prefix="/trip-variance-marks",
    tags=["trip-variance-marks"],
)

_PERM = "can_manage_trip_variance_marks"


class TripVarianceMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    variance_kind: str
    source_ref: str


class TripVarianceMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    variance_kind: str
    source_ref: str


def _as_response(row: TripVarianceMark) -> TripVarianceMarkResponse:
    return TripVarianceMarkResponse.model_validate(row)


@router.get("", response_model=list[TripVarianceMarkResponse])
async def list_trip_variance_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[TripVarianceMarkResponse]:
    rows = await TripVarianceMarkService(session).list_marks()
    return [_as_response(row) for row in rows]


@router.post(
    "",
    response_model=TripVarianceMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_trip_variance_mark(
    body: TripVarianceMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TripVarianceMarkResponse:
    saved = await TripVarianceMarkService(session).persist_trip_variance_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        variance_kind=body.variance_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_response(saved)
