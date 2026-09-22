from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.domain.groupage_tariff import require_postal_zone_kind
from app.models.groupage_tariff import GroupageTariff
from app.services.geography.location_service import LocationService
from app.services.groupage_tariffs.groupage_tariff_service import GroupageTariffService

router = APIRouter(prefix="/groupage-tariffs", tags=["groupage-tariffs"])

_PERM = "can_manage_groupage_tariffs"


class GroupageTariffCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    location_id: UUID
    tariff_code: str
    chargeable_weight: str
    amount: str
    currency: str
    source_ref: str
    volume_m3: str | None = None


class GroupageTariffResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    location_id: UUID
    tariff_code: str
    chargeable_weight: str
    amount: str
    currency: str
    source_ref: str
    volume_m3: str | None


def _as_row(row: GroupageTariff) -> GroupageTariffResponse:
    return GroupageTariffResponse(
        id=row.id,
        organization_id=row.organization_id,
        location_id=row.location_id,
        tariff_code=row.tariff_code,
        chargeable_weight=format(row.chargeable_weight, "f"),
        amount=format(row.amount, "f"),
        currency=str(row.currency).strip(),
        source_ref=row.source_ref,
        volume_m3=None if row.volume_m3 is None else format(row.volume_m3, "f"),
    )


@router.get("", response_model=list[GroupageTariffResponse])
async def list_groupage_tariffs(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[GroupageTariffResponse]:
    rows = await GroupageTariffService(session).list_tariffs()
    return [_as_row(row) for row in rows]


@router.post("", response_model=GroupageTariffResponse, status_code=status.HTTP_201_CREATED)
async def create_groupage_tariff(
    body: GroupageTariffCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> GroupageTariffResponse:
    place = await LocationService(session).get_location(body.location_id)
    require_postal_zone_kind(place.kind)
    row = await GroupageTariffService(session).record_tariff(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        location_id=place.id,
        tariff_code=body.tariff_code,
        chargeable_weight=body.chargeable_weight,
        amount=body.amount,
        currency=body.currency,
        source_ref=body.source_ref,
        volume_m3=body.volume_m3,
    )
    await session.commit()
    return _as_row(row)
