from datetime import date
from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import NbpRateConflict, ResourceNotFound, UnknownNbpRate
from app.domain.nbp_rate import normalize_currency, normalize_nbp_mid, normalize_rate_date
from app.models.nbp_rate import NbpRate
from app.repositories.nbp_rates.nbp_rate_repository import NbpRateRepository

_MANUAL = "tenant:manual"


class NbpRateService:
    def __init__(self, session: AsyncSession) -> None:
        self._rates = NbpRateRepository(session)

    async def list_rates(self) -> list[NbpRate]:
        return await self._rates.list_all()

    async def get_rate(self, rate_id: UUID) -> NbpRate:
        found = await self._rates.get(rate_id)
        if found is None:
            raise ResourceNotFound("nieznany kurs")
        return found

    async def create_rate(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        currency: str,
        rate_date: object,
        mid: object,
    ) -> NbpRate:
        token = normalize_currency(currency)
        day = normalize_rate_date(rate_date)
        amount = normalize_nbp_mid(mid)
        existing = await self._rates.find_as_of(token, day)
        if existing is not None and existing.rate_date == day:
            raise NbpRateConflict(f"kurs {token} na {day.isoformat()} już istnieje")
        row = NbpRate(
            id=uuid4(),
            organization_id=organization_id,
            currency=token,
            rate_date=day,
            mid=amount,
            source_ref=_MANUAL,
            created_by=user_id,
        )
        try:
            return await self._rates.add(row)
        except IntegrityError as exc:
            raise NbpRateConflict(f"kurs {token} na {day.isoformat()} już istnieje") from exc

    async def resolve(self, currency: str, on_date: date) -> NbpRate:
        token = normalize_currency(currency)
        found = await self._rates.find_as_of(token, on_date)
        if found is None:
            raise UnknownNbpRate(f"brak kursu NBP {token} na {on_date.isoformat()}")
        return found
