from datetime import date
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.carrier_profile import CarrierProfile
from app.models.credit_review import CreditReview as ReviewRow
from app.models.customer_sop import CustomerSop
from app.models.party import Party
from app.models.party_bank_account import PartyBankAccount
from app.models.party_charge_override import PartyChargeOverride
from app.models.party_contact import PartyContact
from app.models.party_email_domain import PartyEmailDomain
from app.models.party_scorecard import PartyScorecard


class PartyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[Party]:
        result = await self._session.scalars(select(Party).order_by(Party.legal_name))
        return list(result.all())

    async def get(self, party_id: UUID) -> Party | None:
        found = await self._session.scalar(select(Party).where(Party.id == party_id))
        return found if isinstance(found, Party) else None

    async def find_by_tax_id(self, tax_id: str) -> Party | None:
        found = await self._session.scalar(select(Party).where(Party.tax_id == tax_id))
        return found if isinstance(found, Party) else None

    async def add(self, row: Party) -> Party:
        self._session.add(row)
        await self._session.flush()
        return row

    async def list_contacts(self, party_id: UUID) -> list[PartyContact]:
        result = await self._session.scalars(
            select(PartyContact)
            .where(PartyContact.party_id == party_id)
            .order_by(PartyContact.name),
        )
        return list(result.all())

    async def add_contact(self, row: PartyContact) -> PartyContact:
        self._session.add(row)
        await self._session.flush()
        return row

    async def get_bank_account(self, account_id: UUID) -> PartyBankAccount | None:
        return await self._session.get(PartyBankAccount, account_id)

    async def list_bank_accounts(self, party_id: UUID) -> list[PartyBankAccount]:
        result = await self._session.scalars(
            select(PartyBankAccount).where(PartyBankAccount.party_id == party_id),
        )
        return list(result.all())

    async def add_bank_account(self, row: PartyBankAccount) -> PartyBankAccount:
        self._session.add(row)
        await self._session.flush()
        return row

    async def list_email_domains(self, party_id: UUID) -> list[PartyEmailDomain]:
        result = await self._session.scalars(
            select(PartyEmailDomain).where(PartyEmailDomain.party_id == party_id),
        )
        return list(result.all())

    async def add_email_domain(self, row: PartyEmailDomain) -> PartyEmailDomain:
        self._session.add(row)
        await self._session.flush()
        return row

    async def find_party_by_email_domain(self, domain: str) -> Party | None:
        found = await self._session.scalar(
            select(Party)
            .join(PartyEmailDomain, PartyEmailDomain.party_id == Party.id)
            .where(PartyEmailDomain.domain == domain),
        )
        return found if isinstance(found, Party) else None

    async def list_charge_overrides(self, party_id: UUID) -> list[PartyChargeOverride]:
        result = await self._session.scalars(
            select(PartyChargeOverride).where(PartyChargeOverride.party_id == party_id),
        )
        return list(result.all())

    async def add_charge_override(self, row: PartyChargeOverride) -> PartyChargeOverride:
        self._session.add(row)
        await self._session.flush()
        return row

    async def get_carrier_profile(self, party_id: UUID) -> CarrierProfile | None:
        found = await self._session.scalar(
            select(CarrierProfile).where(CarrierProfile.party_id == party_id),
        )
        return found if isinstance(found, CarrierProfile) else None

    async def add_carrier_profile(self, row: CarrierProfile) -> CarrierProfile:
        self._session.add(row)
        await self._session.flush()
        return row

    async def get_scorecard(self, party_id: UUID) -> PartyScorecard | None:
        found = await self._session.scalar(
            select(PartyScorecard).where(PartyScorecard.party_id == party_id),
        )
        return found if isinstance(found, PartyScorecard) else None

    async def list_scorecards(self) -> list[PartyScorecard]:
        result = await self._session.scalars(
            select(PartyScorecard).order_by(
                PartyScorecard.response_rate.desc().nulls_last(),
                PartyScorecard.median_response_hours.asc().nulls_last(),
            ),
        )
        return list(result.all())

    async def add_scorecard(self, row: PartyScorecard) -> PartyScorecard:
        self._session.add(row)
        await self._session.flush()
        return row

    async def get_sop(self, sop_id: UUID) -> CustomerSop | None:
        found = await self._session.scalar(select(CustomerSop).where(CustomerSop.id == sop_id))
        return found if isinstance(found, CustomerSop) else None

    async def find_sop_by_party_and_code(self, party_id: UUID, code: str) -> CustomerSop | None:
        found = await self._session.scalar(
            select(CustomerSop).where(
                CustomerSop.party_id == party_id,
                CustomerSop.code == code,
            ),
        )
        return found if isinstance(found, CustomerSop) else None

    async def list_sops(self) -> list[CustomerSop]:
        result = await self._session.scalars(select(CustomerSop).order_by(CustomerSop.title))
        return list(result.all())

    async def approved_sop_blocks_auto(self, party_id: UUID) -> bool:
        found = await self._session.scalar(
            select(CustomerSop.id).where(
                CustomerSop.party_id == party_id,
                CustomerSop.status == "approved",
                CustomerSop.blocks_auto.is_(True),
            ),
        )
        return found is not None

    async def add_sop(self, row: CustomerSop) -> CustomerSop:
        self._session.add(row)
        await self._session.flush()
        return row

    async def get_review(self, review_id: UUID) -> ReviewRow | None:
        found = await self._session.get(ReviewRow, review_id)
        return found if isinstance(found, ReviewRow) else None

    async def list_reviews(self) -> list[ReviewRow]:
        result = await self._session.scalars(
            select(ReviewRow).order_by(ReviewRow.review_date.desc()),
        )
        return list(result.all())

    async def find_review_as_of(self, *, party_id: UUID, on_date: date) -> ReviewRow | None:
        found = await self._session.scalar(
            select(ReviewRow)
            .where(
                ReviewRow.party_id == party_id,
                ReviewRow.review_date <= on_date,
            )
            .order_by(ReviewRow.review_date.desc())
            .limit(1),
        )
        return found if isinstance(found, ReviewRow) else None

    async def add_review(self, row: ReviewRow) -> ReviewRow:
        self._session.add(row)
        await self._session.flush()
        return row
