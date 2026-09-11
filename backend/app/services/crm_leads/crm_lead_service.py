from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.crm_lead import parse_crm_lead_row
from app.models.crm_lead import CrmLead
from app.repositories.crm_leads.crm_lead_repository import CrmLeadRepository


class CrmLeadService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = CrmLeadRepository(session)

    async def list_leads(self) -> list[CrmLead]:
        return await self._rows.list_leads()

    async def persist_crm_lead(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        lead_code: object,
        stage_kind: object,
        source_ref: object,
    ) -> CrmLead:
        code, kind, origin = parse_crm_lead_row(lead_code, stage_kind, source_ref)
        row = CrmLead(
            id=uuid4(),
            organization_id=organization_id,
            lead_code=code,
            stage_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_lead(row)
