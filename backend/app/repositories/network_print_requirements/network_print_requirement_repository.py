from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.network_print_requirement import NetworkPrintRequirement


class NetworkPrintRequirementRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_requirements(self) -> list[NetworkPrintRequirement]:
        packed = await self._session.scalars(
            select(NetworkPrintRequirement).order_by(
                NetworkPrintRequirement.requirement_code,
                NetworkPrintRequirement.id,
            ),
        )
        return list(packed.all())

    async def add_requirement(
        self,
        row: NetworkPrintRequirement,
    ) -> NetworkPrintRequirement:
        self._session.add(row)
        await self._session.flush()
        return row
