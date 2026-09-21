from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.charge import margin
from app.domain.charge_code import normalize_charge_code
from app.domain.errors import (
    ChargeRateMismatch,
    InvalidShipment,
    ResourceNotFound,
    UnknownChargeCode,
)
from app.domain.money import Money
from app.domain.rate_line import require_source_ref
from app.models.charge import Charge
from app.models.charge_code import ChargeCode
from app.repositories.charge_codes.charge_code_repository import ChargeCodeRepository
from app.repositories.charges.charge_repository import ChargeRepository
from app.repositories.rate_lines.rate_line_repository import RateLineRepository


class ChargeService:
    def __init__(self, session: AsyncSession) -> None:
        self._charges = ChargeRepository(session)
        self._codes = ChargeCodeRepository(session)
        self._rates = RateLineRepository(session)

    async def list_charges(self) -> list[tuple[Charge, Decimal]]:
        return await self._charges.list_with_sql_margin()

    async def get_charge(self, charge_id: UUID) -> Charge:
        found = await self._charges.get(charge_id)
        if found is None:
            raise ResourceNotFound("nieznana opłata")
        return found

    async def create_charge(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        charge_code: str,
        buy_amount: object,
        buy_currency: object,
        sell_amount: object,
        sell_currency: object,
        rate_line_id: UUID | None,
        source_ref: object,
        shipment_id: UUID | None = None,
    ) -> Charge:
        origin = require_source_ref(source_ref)
        buy = Money.of(buy_amount, buy_currency)
        sell = Money.of(sell_amount, sell_currency)
        margin(buy, sell)
        catalog = await self._require_catalog(charge_code)
        linked = await self._optional_buy_rate(rate_line_id, catalog.code)
        row = Charge(
            id=uuid4(),
            organization_id=organization_id,
            charge_code=catalog.code,
            buy_amount=buy.amount,
            buy_currency=buy.currency.code,
            sell_amount=sell.amount,
            sell_currency=sell.currency.code,
            rate_line_id=linked,
            shipment_id=shipment_id,
            source_ref=origin,
            created_by=user_id,
        )
        try:
            return await self._charges.add(row)
        except IntegrityError as exc:
            if shipment_id is not None and "fk_charge_shipment" in str(exc.orig):
                raise InvalidShipment("zlecenie") from exc
            raise

    async def _require_catalog(self, charge_code: str) -> ChargeCode:
        token = normalize_charge_code(charge_code)
        catalog = await self._codes.find_by_token(token)
        if catalog is None:
            raise UnknownChargeCode(f"nieznany kod opłaty: {token}")
        return catalog

    async def _optional_buy_rate(self, rate_line_id: UUID | None, charge_code: str) -> UUID | None:
        if rate_line_id is None:
            return None
        rate = await self._rates.get(rate_line_id)
        if rate is None:
            raise ResourceNotFound("rate_line nie istnieje")
        if rate.charge_code != charge_code:
            raise ChargeRateMismatch("charge_code musi zgadzać się ze stawką kupna")
        return rate.id
