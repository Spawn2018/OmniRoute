from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.telematics_device import TelematicsDevice


class TelematicsDeviceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_devices(self) -> list[TelematicsDevice]:
        packed = await self._session.scalars(
            select(TelematicsDevice).order_by(
                TelematicsDevice.device_code,
                TelematicsDevice.id,
            ),
        )
        return list(packed.all())

    async def add_device(self, row: TelematicsDevice) -> TelematicsDevice:
        self._session.add(row)
        await self._session.flush()
        return row
