from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.organization_setting import normalize_setting_key, normalize_setting_value
from app.models.organization_setting import OrganizationSetting
from app.repositories.organization_settings.organization_setting_repository import (
    OrganizationSettingRepository,
)


class OrganizationSettingService:
    def __init__(self, session: AsyncSession) -> None:
        self._settings = OrganizationSettingRepository(session)

    async def list_settings(self) -> list[OrganizationSetting]:
        return await self._settings.list_all()

    async def upsert_setting(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        setting_key: str,
        setting_value: str,
    ) -> OrganizationSetting:
        token = normalize_setting_key(setting_key)
        stored_value = normalize_setting_value(token, setting_value)
        existing = await self._settings.find_by_key(token)
        if existing is not None:
            existing.setting_value = stored_value
            existing.created_by = user_id
            await self._settings.flush()
            return existing
        row = OrganizationSetting(
            id=uuid4(),
            organization_id=organization_id,
            setting_key=token,
            setting_value=stored_value,
            created_by=user_id,
        )
        return await self._settings.add(row)
