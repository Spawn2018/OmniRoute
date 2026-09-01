from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import (
    PortSurchargeConflict,
    UnknownPort,
    UnknownPortSurcharge,
)
from app.domain.port_surcharge import (
    normalize_applies_when,
    normalize_surcharge_amount,
    normalize_surcharge_code,
    normalize_surcharge_currency,
    normalize_surcharge_title,
)
from app.models.port_surcharge import PortSurcharge
from app.repositories.port_surcharges.port_surcharge_repository import PortSurchargeRepository

_MANUAL = "tenant:manual"


class PortSurchargeService:
    def __init__(self, session: AsyncSession) -> None:
        self._extras = PortSurchargeRepository(session)

    async def list_surcharges(self) -> list[PortSurcharge]:
        return await self._extras.list_all()

    async def resolve(self, port_id: UUID, code: object) -> PortSurcharge:
        token = normalize_surcharge_code(code)
        await self._require_port(port_id)
        found = await self._extras.find_by_port_and_code(port_id, token)
        if found is None:
            raise UnknownPortSurcharge(f"nieznane extra portowe: {token}")
        return found

    async def create_surcharge(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        port_id: UUID,
        code: object,
        title: object,
        applies_when: object,
        amount: object,
        currency: object,
    ) -> PortSurcharge:
        token = normalize_surcharge_code(code)
        heading = normalize_surcharge_title(title)
        when = normalize_applies_when(applies_when)
        stored_amount = normalize_surcharge_amount(amount)
        iso = normalize_surcharge_currency(currency)
        await self._require_port(port_id)
        duplicate = await self._extras.find_by_port_and_code(port_id, token)
        if duplicate is not None:
            raise PortSurchargeConflict(f"extra {token} już istnieje")
        row = PortSurcharge(
            id=uuid4(),
            organization_id=organization_id,
            amount=stored_amount,
            currency=iso,
            port_id=port_id,
            code=token,
            title=heading,
            applies_when=when,
            source_ref=_MANUAL,
            created_by=user_id,
        )
        try:
            return await self._extras.add(row)
        except IntegrityError as exc:
            raise PortSurchargeConflict(f"extra {token} już istnieje") from exc

    async def _require_port(self, port_id: UUID) -> None:
        found = await self._extras.get_port(port_id)
        if found is None:
            raise UnknownPort(f"nieznany port: {port_id}")
