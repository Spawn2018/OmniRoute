from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.cod_instruction import (
    require_collection_status,
    require_instruction_code,
    require_instruction_shipment_id,
    require_instruction_source_ref,
)
from app.models.cod_instruction import CodInstruction
from app.repositories.cod_instructions.cod_instruction_repository import (
    CodInstructionRepository,
)


class CodInstructionService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = CodInstructionRepository(session)

    async def list_instructions(self) -> list[CodInstruction]:
        return await self._rows.list_all()

    async def record_instruction(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        shipment_id: object,
        instruction_code: object,
        collection_status: object,
        source_ref: object,
    ) -> CodInstruction:
        row = CodInstruction(
            id=uuid4(),
            organization_id=organization_id,
            shipment_id=require_instruction_shipment_id(shipment_id),
            instruction_code=require_instruction_code(instruction_code),
            collection_status=require_collection_status(collection_status),
            source_ref=require_instruction_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._rows.add(row)
