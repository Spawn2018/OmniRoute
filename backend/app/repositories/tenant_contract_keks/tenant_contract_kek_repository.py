from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tenant_contract_kek import TenantContractKek


class TenantContractKekRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[TenantContractKek]:
        packed = await self._session.scalars(
            select(TenantContractKek).order_by(
                TenantContractKek.wrap_kind,
                TenantContractKek.kek_code,
                TenantContractKek.id,
            ),
        )
        return list(packed.all())

    async def insert_mark(self, mark: TenantContractKek) -> TenantContractKek:
        self._session.add(mark)
        await self._session.flush()
        return mark
