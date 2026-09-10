from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer_contract import CustomerContract


class CustomerContractRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_rows(self) -> list[CustomerContract]:
        packed = await self._session.scalars(
            select(CustomerContract).order_by(
                CustomerContract.contract_code,
                CustomerContract.id,
            ),
        )
        return list(packed.all())

    async def add(self, row: CustomerContract) -> CustomerContract:
        self._session.add(row)
        await self._session.flush()
        return row
