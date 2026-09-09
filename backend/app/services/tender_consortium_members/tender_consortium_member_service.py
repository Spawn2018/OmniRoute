from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.tender_consortium_member import (
    require_board_id,
    require_party_id,
    require_seat_code,
    require_seat_source_ref,
)
from app.models.tender_consortium_member import TenderConsortiumMember
from app.repositories.tender_consortium_members.tender_consortium_member_repository import (
    TenderConsortiumMemberRepository,
)


class TenderConsortiumMemberService:
    def __init__(self, session: AsyncSession) -> None:
        self._seats = TenderConsortiumMemberRepository(session)

    async def list_seats(self) -> list[TenderConsortiumMember]:
        return await self._seats.fetch_seats()

    async def persist_seat(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        tender_id: object,
        party_id: object,
        seat_code: object,
        source_ref: object,
    ) -> TenderConsortiumMember:
        row = TenderConsortiumMember(
            id=uuid4(),
            organization_id=organization_id,
            tender_id=require_board_id(tender_id),
            party_id=require_party_id(party_id),
            seat_code=require_seat_code(seat_code),
            source_ref=require_seat_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._seats.add(row)
