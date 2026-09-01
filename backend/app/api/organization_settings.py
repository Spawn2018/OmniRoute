from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.organization_setting import OrganizationSetting
from app.services.organization_settings.organization_setting_service import (
    OrganizationSettingService,
)

router = APIRouter(prefix="/organization-settings", tags=["organization-settings"])


class OrganizationSettingUpsert(BaseModel):
    setting_key: str = Field(min_length=1, max_length=64)
    setting_value: str = Field(min_length=1, max_length=64)


class OrganizationSettingResponse(BaseModel):
    id: UUID
    organization_id: UUID
    setting_key: str
    setting_value: str

    @classmethod
    def from_row(cls, row: OrganizationSetting) -> "OrganizationSettingResponse":
        return cls(
            id=row.id,
            organization_id=row.organization_id,
            setting_key=row.setting_key,
            setting_value=row.setting_value,
        )


@router.get("", response_model=list[OrganizationSettingResponse])
async def list_organization_settings(
    _authz: None = Depends(require_permission("can_manage_organization_settings", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[OrganizationSettingResponse]:
    service = OrganizationSettingService(session)
    rows = await service.list_settings()
    return [OrganizationSettingResponse.from_row(row) for row in rows]


@router.put("", response_model=OrganizationSettingResponse)
async def upsert_organization_setting(
    body: OrganizationSettingUpsert,
    _authz: None = Depends(require_permission("can_manage_organization_settings", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> OrganizationSettingResponse:
    service = OrganizationSettingService(session)
    row = await service.upsert_setting(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        setting_key=body.setting_key,
        setting_value=body.setting_value,
    )
    await session.commit()
    return OrganizationSettingResponse.from_row(row)
