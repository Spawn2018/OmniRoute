from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.network_print_requirement import parse_network_print_requirement_row
from app.models.network_print_requirement import NetworkPrintRequirement
from app.repositories.network_print_requirements.network_print_requirement_repository import (
    NetworkPrintRequirementRepository,
)


class NetworkPrintRequirementService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = NetworkPrintRequirementRepository(session)

    async def list_requirements(self) -> list[NetworkPrintRequirement]:
        return await self._rows.list_requirements()

    async def persist_network_print_requirement(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        requirement_code: object,
        network_label: object,
        source_ref: object,
    ) -> NetworkPrintRequirement:
        code, label, origin = parse_network_print_requirement_row(
            requirement_code,
            network_label,
            source_ref,
        )
        row = NetworkPrintRequirement(
            id=uuid4(),
            organization_id=organization_id,
            requirement_code=code,
            network_label=label,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_requirement(row)
