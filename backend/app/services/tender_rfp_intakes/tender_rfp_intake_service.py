from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.tender_rfp_intake import (
    require_board_id,
    require_intake_code,
    require_intake_source_ref,
)
from app.models.tender_rfp_intake import TenderRfpIntake
from app.repositories.tender_rfp_intakes.tender_rfp_intake_repository import (
    TenderRfpIntakeRepository,
)


class TenderRfpIntakeService:
    def __init__(self, session: AsyncSession) -> None:
        self._intakes = TenderRfpIntakeRepository(session)

    async def list_intakes(self) -> list[TenderRfpIntake]:
        return await self._intakes.fetch_intakes()

    async def persist_intake(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        tender_id: object,
        intake_code: object,
        source_ref: object,
    ) -> TenderRfpIntake:
        row = TenderRfpIntake(
            id=uuid4(),
            organization_id=organization_id,
            tender_id=require_board_id(tender_id),
            intake_code=require_intake_code(intake_code),
            source_ref=require_intake_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._intakes.add(row)
