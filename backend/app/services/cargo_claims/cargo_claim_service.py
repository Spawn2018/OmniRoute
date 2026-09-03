from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.cargo_claim import (
    require_claim_kind,
    require_claim_shipment_id,
    require_claim_source_ref,
)
from app.models.cargo_claim import CargoClaim
from app.repositories.cargo_claims.cargo_claim_repository import CargoClaimRepository


class CargoClaimService:
    def __init__(self, session: AsyncSession) -> None:
        self._claims = CargoClaimRepository(session)

    async def list_claims(self) -> list[CargoClaim]:
        return await self._claims.list_all()

    async def record_claim(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        shipment_id: UUID,
        claim_kind: str,
        source_ref: str,
    ) -> CargoClaim:
        row = CargoClaim(
            id=uuid4(),
            organization_id=organization_id,
            shipment_id=require_claim_shipment_id(shipment_id),
            claim_kind=require_claim_kind(claim_kind),
            source_ref=require_claim_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._claims.add(row)
