from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.charge_code import normalize_charge_code
from app.domain.errors import QuotationGap, UnknownChargeCode
from app.models.charge_code import ChargeCode
from app.models.quotation import Quotation
from app.repositories.charge_codes.charge_code_repository import ChargeCodeRepository
from app.repositories.quotations.quotation_repository import QuotationRepository


class QuotationService:
    def __init__(self, session: AsyncSession) -> None:
        self._quotations = QuotationRepository(session)
        self._codes = ChargeCodeRepository(session)

    async def list_quotations(self) -> list[Quotation]:
        return await self._quotations.list_all()

    async def quote_from_current_rate(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        charge_code: str,
    ) -> Quotation:
        catalog = await self._require_catalog(charge_code)
        quoted = await self._quotations.insert_from_current_rate(
            organization_id=organization_id,
            created_by=user_id,
            charge_code=catalog.code,
        )
        if quoted is None:
            raise QuotationGap(f"quotation_gap: brak bieżącej stawki dla {catalog.code}")
        return quoted

    async def _require_catalog(self, charge_code: str) -> ChargeCode:
        token = normalize_charge_code(charge_code)
        catalog = await self._codes.find_by_token(token)
        if catalog is None:
            raise UnknownChargeCode(f"nieznany kod opłaty: {token}")
        return catalog
