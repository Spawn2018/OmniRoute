from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.charge_code import normalize_charge_code
from app.domain.errors import (
    InvalidRateLine,
    RateLineAlreadySuperseded,
    ResourceNotFound,
    UnknownChargeCode,
)
from app.domain.money import Money
from app.domain.rate_line import (
    require_allotment_teu,
    require_fuel_index_id,
    require_index_id,
    require_source_ref,
    require_spot_or_contract,
)
from app.models.rate_line import RateLine
from app.repositories.charge_codes.charge_code_repository import ChargeCodeRepository
from app.repositories.fuel_indexes.fuel_index_repository import FuelIndexRepository
from app.repositories.rate_lines.rate_line_repository import RateLineRepository


class RateLineService:
    def __init__(self, session: AsyncSession) -> None:
        self._rates = RateLineRepository(session)
        self._codes = ChargeCodeRepository(session)
        self._indexes = FuelIndexRepository(session)

    async def list_rates(self) -> list[RateLine]:
        return await self._rates.list_all()

    async def _bound_fuel_index(self, fuel_index_id: object) -> UUID | None:
        index_fk = require_fuel_index_id(fuel_index_id)
        if index_fk is None:
            return None
        if await self._indexes.get(index_fk) is None:
            raise InvalidRateLine("nieznany fuel_index")
        return index_fk

    async def _catalog_code(self, charge_code: str) -> str:
        token = normalize_charge_code(charge_code)
        catalog = await self._codes.find_by_token(token)
        if catalog is None:
            raise UnknownChargeCode(f"nieznany kod opłaty: {token}")
        return catalog.code

    async def create_buy_rate(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        charge_code: str,
        amount: object,
        currency: object,
        source_ref: str,
        allotment_teu: object = None,
        spot_or_contract: object = None,
        index_id: object = None,
        fuel_index_id: object = None,
    ) -> RateLine:
        origin = require_source_ref(source_ref)
        money = Money.of(amount, currency)
        index_fk = await self._bound_fuel_index(fuel_index_id)
        code = await self._catalog_code(charge_code)
        row = RateLine(
            id=uuid4(),
            organization_id=organization_id,
            charge_code=code,
            amount=money.amount,
            currency=money.currency.code,
            allotment_teu=require_allotment_teu(allotment_teu),
            spot_or_contract=require_spot_or_contract(spot_or_contract),
            index_id=require_index_id(index_id),
            fuel_index_id=index_fk,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rates.add(row)

    async def supersede(
        self,
        *,
        rate_line_id: UUID,
        user_id: UUID,
        amount: object,
        currency: object,
        source_ref: str,
        allotment_teu: object = None,
        spot_or_contract: object = None,
        index_id: object = None,
        fuel_index_id: object = None,
    ) -> RateLine:
        current = await self._rates.get(rate_line_id)
        if current is None:
            raise ResourceNotFound("rate_line nie istnieje")
        if current.superseded_by is not None:
            raise RateLineAlreadySuperseded("rate_line już zastąpiony")
        successor = await self.create_buy_rate(
            organization_id=current.organization_id,
            user_id=user_id,
            charge_code=current.charge_code,
            amount=amount,
            currency=currency,
            source_ref=source_ref,
            allotment_teu=allotment_teu,
            spot_or_contract=spot_or_contract,
            index_id=index_id,
            fuel_index_id=fuel_index_id,
        )
        await self._rates.mark_superseded(current, successor.id)
        return successor
