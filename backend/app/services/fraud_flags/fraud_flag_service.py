from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.fraud_flag import (
    require_flag_kind,
    require_flag_party_id,
    require_flag_source_ref,
)
from app.models.fraud_flag import FraudFlag
from app.repositories.fraud_flags.fraud_flag_repository import FraudFlagRepository


class FraudFlagService:
    def __init__(self, session: AsyncSession) -> None:
        self._flags = FraudFlagRepository(session)

    async def list_flags(self) -> list[FraudFlag]:
        return await self._flags.list_all()

    async def record_flag(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        party_id: UUID,
        flag_kind: str,
        source_ref: str,
    ) -> FraudFlag:
        row = FraudFlag(
            id=uuid4(),
            organization_id=organization_id,
            party_id=require_flag_party_id(party_id),
            flag_kind=require_flag_kind(flag_kind),
            source_ref=require_flag_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._flags.add(row)
