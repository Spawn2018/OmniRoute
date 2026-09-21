from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.domain.organization_calendar import require_country_code
from app.models.organization_calendar import OrganizationCalendar
from app.services.organization_calendars.organization_calendar_service import (
    OrganizationCalendarService,
)

router = APIRouter(prefix="/organization-calendars", tags=["organization-calendars"])

_SETTINGS = "can_manage_organization_settings"


class OrganizationCalendarCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    country_code: str
    calendar_day: date
    day_kind: str
    source_ref: str


class OrganizationCalendarResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    country_code: str
    calendar_day: date
    day_kind: str
    source_ref: str
    superseded_by: UUID | None

    @classmethod
    def from_row(cls, row: OrganizationCalendar) -> "OrganizationCalendarResponse":
        return cls(
            id=row.id,
            organization_id=row.organization_id,
            country_code=row.country_code,
            calendar_day=row.calendar_day,
            day_kind=row.day_kind,
            source_ref=row.source_ref,
            superseded_by=row.superseded_by,
        )


class WorkingDayResponse(BaseModel):
    country_code: str
    calendar_day: date
    is_working_day: bool


class FxRateDayResponse(BaseModel):
    country_code: str
    anchor: date
    offset_days: str
    fx_rate_day: date


@router.get("", response_model=list[OrganizationCalendarResponse])
async def list_organization_calendars(
    country_code: str = Query(...),
    _authz: None = Depends(require_permission(_SETTINGS, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[OrganizationCalendarResponse]:
    rows = await OrganizationCalendarService(session).list_for_country(country_code=country_code)
    return [OrganizationCalendarResponse.from_row(row) for row in rows]


@router.get("/working-day", response_model=WorkingDayResponse)
async def get_working_day(
    country_code: str = Query(...),
    calendar_day: date = Query(...),
    _authz: None = Depends(require_permission(_SETTINGS, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> WorkingDayResponse:
    code = require_country_code(country_code)
    flagged = await OrganizationCalendarService(session).is_working_day(
        country_code=code,
        calendar_day=calendar_day,
    )
    return WorkingDayResponse(
        country_code=code,
        calendar_day=calendar_day,
        is_working_day=flagged,
    )


@router.get("/fx-rate-day", response_model=FxRateDayResponse)
async def get_fx_rate_day(
    country_code: str = Query(...),
    anchor: date = Query(...),
    offset_days: str = Query(...),
    _authz: None = Depends(require_permission(_SETTINGS, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> FxRateDayResponse:
    code = require_country_code(country_code)
    resolved = await OrganizationCalendarService(session).fx_rate_day(
        country_code=code,
        anchor=anchor,
        offset_days=offset_days,
    )
    return FxRateDayResponse(
        country_code=code,
        anchor=anchor,
        offset_days=offset_days.strip(),
        fx_rate_day=resolved,
    )


@router.post(
    "",
    response_model=OrganizationCalendarResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_organization_calendar(
    body: OrganizationCalendarCreate,
    _authz: None = Depends(require_permission(_SETTINGS, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> OrganizationCalendarResponse:
    row = await OrganizationCalendarService(session).record_day(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        country_code=body.country_code,
        calendar_day=body.calendar_day,
        day_kind=body.day_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return OrganizationCalendarResponse.from_row(row)
