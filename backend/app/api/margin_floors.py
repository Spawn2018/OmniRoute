"""HTTP podłoga marży — HITL Decimal + UN/LOCODE, bez 409 na charge."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.margin_floor import MarginFloor
from app.services.margin_floors.margin_floor_service import MarginFloorService

router = APIRouter(prefix="/margin-floors", tags=["margin-floors"])
_PERM = "can_manage_margin_floors"


class MarginFloorCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    floor_code: str = Field(min_length=2, max_length=32)
    origin_unlocode: str = Field(min_length=5, max_length=5)
    destination_unlocode: str = Field(min_length=5, max_length=5)
    floor_amount: str
    floor_currency: str = Field(min_length=3, max_length=3)
    source_ref: str = Field(min_length=1, max_length=256)


class MarginFloorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    floor_code: str
    origin_unlocode: str
    destination_unlocode: str
    floor_amount: str
    floor_currency: str
    source_ref: str


def _as_row(row: MarginFloor) -> MarginFloorResponse:
    return MarginFloorResponse(
        id=row.id,
        organization_id=row.organization_id,
        floor_code=row.floor_code,
        origin_unlocode=row.origin_unlocode,
        destination_unlocode=row.destination_unlocode,
        floor_amount=format(row.floor_amount, "f"),
        floor_currency=row.floor_currency,
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[MarginFloorResponse])
async def list_margin_floors(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[MarginFloorResponse]:
    rows = await MarginFloorService(session).list_rows()
    return [_as_row(row) for row in rows]


@router.post(
    "",
    response_model=MarginFloorResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_margin_floor(
    body: MarginFloorCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> MarginFloorResponse:
    saved = await MarginFloorService(session).persist_floor(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        floor_code=body.floor_code,
        origin_unlocode=body.origin_unlocode,
        destination_unlocode=body.destination_unlocode,
        floor_amount=body.floor_amount,
        floor_currency=body.floor_currency,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "margin-floor"
    response.headers["X-Omni-Mode"] = "hitl"
    return _as_row(saved)
