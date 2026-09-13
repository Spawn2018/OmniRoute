from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.telematics_device import parse_telematics_device_row
from app.models.telematics_device import TelematicsDevice
from app.repositories.telematics_devices.telematics_device_repository import (
    TelematicsDeviceRepository,
)


class TelematicsDeviceService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = TelematicsDeviceRepository(session)

    async def list_devices(self) -> list[TelematicsDevice]:
        return await self._rows.list_devices()

    async def persist_telematics_device(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        device_code: object,
        device_kind: object,
        source_ref: object,
    ) -> TelematicsDevice:
        code, kind, origin = parse_telematics_device_row(
            device_code,
            device_kind,
            source_ref,
        )
        row = TelematicsDevice(
            id=uuid4(),
            organization_id=organization_id,
            device_code=code,
            device_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_device(row)
