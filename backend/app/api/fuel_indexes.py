from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.fuel_index import FuelIndex
from app.services.fuel_indexes.fuel_index_service import FuelIndexService

router = APIRouter(prefix="/fuel-indexes", tags=["fuel-indexes"])

_PERM = "can_manage_fuel_indexes"


class FuelIndexCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    index_kind: str
    published_on: str
    index_value: str
    source_ref: str


class FuelIndexResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    index_kind: str
    published_on: str
    index_value: str
    source_ref: str


def _as_row(row: FuelIndex) -> FuelIndexResponse:
    return FuelIndexResponse(
        id=row.id,
        organization_id=row.organization_id,
        index_kind=row.index_kind,
        published_on=row.published_on.isoformat(),
        index_value=format(row.index_value, "f"),
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[FuelIndexResponse])
async def list_fuel_indexes(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[FuelIndexResponse]:
    rows = await FuelIndexService(session).list_indexes()
    return [_as_row(row) for row in rows]


@router.post("", response_model=FuelIndexResponse, status_code=status.HTTP_201_CREATED)
async def create_fuel_index(
    body: FuelIndexCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> FuelIndexResponse:
    row = await FuelIndexService(session).record_index(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        index_kind=body.index_kind,
        published_on=body.published_on,
        index_value=body.index_value,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
