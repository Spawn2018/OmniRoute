from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.organization_setting import OrganizationSetting


class OrganizationSettingRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[OrganizationSetting]:
        result = await self._session.scalars(
            select(OrganizationSetting).order_by(OrganizationSetting.setting_key),
        )
        return list(result.all())

    async def find_by_key(self, setting_key: str) -> OrganizationSetting | None:
        found = await self._session.scalar(
            select(OrganizationSetting).where(OrganizationSetting.setting_key == setting_key),
        )
        return found if isinstance(found, OrganizationSetting) else None

    async def add(self, row: OrganizationSetting) -> OrganizationSetting:
        self._session.add(row)
        await self._session.flush()
        return row

    async def flush(self) -> None:
        await self._session.flush()
