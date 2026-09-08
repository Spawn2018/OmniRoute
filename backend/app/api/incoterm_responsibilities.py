from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.incoterm_responsibility import IncotermResponsibility
from app.services.incoterm_responsibilities.incoterm_responsibility_service import (
    IncotermResponsibilityService,
)

router = APIRouter(prefix="/incoterm-responsibilities", tags=["incoterm-responsibilities"])


class IncotermResponsibilityCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    incoterm: str
    trade_side: str
    export_clearance_role: str
    import_clearance_role: str
    main_carriage_booker: str
    booking_scope: list[str]
    source_ref: str


class IncotermResponsibilityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    incoterm: str
    trade_side: str
    export_clearance_role: str
    import_clearance_role: str
    main_carriage_booker: str
    booking_scope: list[str]
    source_ref: str
    superseded_by: UUID | None

    @classmethod
    def from_row(cls, row: IncotermResponsibility) -> "IncotermResponsibilityResponse":
        return cls(
            id=row.id,
            organization_id=row.organization_id,
            incoterm=str(row.incoterm).strip(),
            trade_side=row.trade_side,
            export_clearance_role=row.export_clearance_role,
            import_clearance_role=row.import_clearance_role,
            main_carriage_booker=row.main_carriage_booker,
            booking_scope=list(row.booking_scope),
            source_ref=row.source_ref,
            superseded_by=row.superseded_by,
        )


@router.get("", response_model=list[IncotermResponsibilityResponse])
async def list_incoterm_responsibilities(
    incoterm: str = Query(...),
    trade_side: str = Query(...),
    _authz: None = Depends(require_permission("can_manage_quotations", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[IncotermResponsibilityResponse]:
    rows = await IncotermResponsibilityService(session).list_for_pair(
        incoterm=incoterm,
        trade_side=trade_side,
    )
    return [IncotermResponsibilityResponse.from_row(row) for row in rows]


@router.post(
    "",
    response_model=IncotermResponsibilityResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_incoterm_responsibility(
    body: IncotermResponsibilityCreate,
    _authz: None = Depends(require_permission("can_manage_quotations", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> IncotermResponsibilityResponse:
    row = await IncotermResponsibilityService(session).record_rule(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        incoterm=body.incoterm,
        trade_side=body.trade_side,
        export_clearance_role=body.export_clearance_role,
        import_clearance_role=body.import_clearance_role,
        main_carriage_booker=body.main_carriage_booker,
        booking_scope=body.booking_scope,
        source_ref=body.source_ref,
    )
    await session.commit()
    return IncotermResponsibilityResponse.from_row(row)


@router.post(
    "/seed",
    response_model=list[IncotermResponsibilityResponse],
    status_code=status.HTTP_201_CREATED,
)
async def seed_incoterm_responsibilities(
    _authz: None = Depends(require_permission("can_manage_quotations", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> list[IncotermResponsibilityResponse]:
    rows = await IncotermResponsibilityService(session).seed_omni_ops(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
    )
    await session.commit()
    return [IncotermResponsibilityResponse.from_row(row) for row in rows]
