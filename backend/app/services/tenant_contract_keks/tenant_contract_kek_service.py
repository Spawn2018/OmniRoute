from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.tenant_contract_kek import (
    require_kek_code,
    require_kek_source_ref,
    require_wrap_kind,
)
from app.models.tenant_contract_kek import TenantContractKek
from app.repositories.tenant_contract_keks.tenant_contract_kek_repository import (
    TenantContractKekRepository,
)


class TenantContractKekService:
    def __init__(self, session: AsyncSession) -> None:
        self._marks = TenantContractKekRepository(session)

    async def list_marks(self) -> list[TenantContractKek]:
        return await self._marks.list_marks()

    async def persist_kek_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        kek_code: object,
        wrap_kind: object,
        source_ref: object,
    ) -> TenantContractKek:
        mark = TenantContractKek(
            id=uuid4(),
            organization_id=organization_id,
            kek_code=require_kek_code(kek_code),
            wrap_kind=require_wrap_kind(wrap_kind),
            source_ref=require_kek_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._marks.insert_mark(mark)
