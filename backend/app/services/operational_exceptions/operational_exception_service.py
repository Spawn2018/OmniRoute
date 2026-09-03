from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.operational_exception import (
    require_exception_kind,
    require_exception_shipment_id,
    require_exception_source_ref,
)
from app.models.operational_exception import OperationalException
from app.repositories.operational_exceptions.operational_exception_repository import (
    OperationalExceptionRepository,
)


class OperationalExceptionService:
    def __init__(self, session: AsyncSession) -> None:
        self._exceptions = OperationalExceptionRepository(session)

    async def list_exceptions(self) -> list[OperationalException]:
        return await self._exceptions.list_all()

    async def record_exception(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        shipment_id: UUID,
        exception_kind: str,
        source_ref: str,
    ) -> OperationalException:
        row = OperationalException(
            id=uuid4(),
            organization_id=organization_id,
            shipment_id=require_exception_shipment_id(shipment_id),
            exception_kind=require_exception_kind(exception_kind),
            source_ref=require_exception_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._exceptions.add(row)
