from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.charge_template import ChargeTemplate
from app.services.charge_templates.charge_template_service import ChargeTemplateService

router = APIRouter(prefix="/charge-templates", tags=["charge-templates"])

_PERM = "can_manage_charge_templates"


class ChargeTemplateCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    template_code: str
    charge_code: str
    valid_from: str
    valid_until: str
    source_ref: str


class ChargeTemplateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    template_code: str
    charge_code: str
    valid_from: str
    valid_until: str
    source_ref: str


def _as_row(row: ChargeTemplate) -> ChargeTemplateResponse:
    return ChargeTemplateResponse(
        id=row.id,
        organization_id=row.organization_id,
        template_code=row.template_code,
        charge_code=row.charge_code,
        valid_from=row.valid_from.isoformat(),
        valid_until=row.valid_until.isoformat(),
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[ChargeTemplateResponse])
async def list_charge_templates(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ChargeTemplateResponse]:
    rows = await ChargeTemplateService(session).list_templates()
    return [_as_row(row) for row in rows]


@router.post("", response_model=ChargeTemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_charge_template(
    body: ChargeTemplateCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ChargeTemplateResponse:
    row = await ChargeTemplateService(session).record_template(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        template_code=body.template_code,
        charge_code=body.charge_code,
        valid_from=body.valid_from,
        valid_until=body.valid_until,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
