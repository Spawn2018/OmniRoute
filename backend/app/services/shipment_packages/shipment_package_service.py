from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.shipment_package import (
    require_package_code,
    require_package_source_ref,
    require_package_status,
    require_package_uuid,
    require_scan_token,
)
from app.models.shipment_package import ShipmentPackage
from app.repositories.shipment_packages.shipment_package_repository import (
    ShipmentPackageRepository,
)


class ShipmentPackageService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = ShipmentPackageRepository(session)

    async def list_packages(self) -> list[ShipmentPackage]:
        return await self._rows.list_all()

    async def record_package(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        shipment_id: object,
        stop_id: object,
        package_code: object,
        package_status: object,
        scan_token: object,
        source_ref: object,
    ) -> ShipmentPackage:
        code = require_package_code(package_code)
        row = ShipmentPackage(
            id=uuid4(),
            organization_id=organization_id,
            shipment_id=require_package_uuid(shipment_id, field="shipment_id"),
            stop_id=require_package_uuid(stop_id, field="stop_id"),
            package_code=code,
            package_status=require_package_status(package_status),
            scan_token=require_scan_token(scan_token, code),
            source_ref=require_package_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._rows.add(row)
