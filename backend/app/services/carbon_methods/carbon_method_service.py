from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.carbon_method import (
    require_carbon_method_source_ref,
    require_method_code,
    require_method_version,
)
from app.models.carbon_method import CarbonMethod
from app.repositories.carbon_methods.carbon_method_repository import (
    CarbonMethodRepository,
)


class CarbonMethodService:
    def __init__(self, session: AsyncSession) -> None:
        self._methods = CarbonMethodRepository(session)

    async def list_methods(self) -> list[CarbonMethod]:
        return await self._methods.fetch_methods()

    async def persist_method(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        method_code: object,
        method_version: object,
        source_ref: object,
    ) -> CarbonMethod:
        row = CarbonMethod(
            id=uuid4(),
            organization_id=organization_id,
            method_code=require_method_code(method_code),
            method_version=require_method_version(method_version),
            source_ref=require_carbon_method_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._methods.add(row)
