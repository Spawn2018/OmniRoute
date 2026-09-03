from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.bank_payment import (
    require_payment_account_id,
    require_payment_invoice_id,
    require_payment_source_ref,
)
from app.domain.errors import InvalidBankPayment
from app.models.bank_payment import BankPayment
from app.repositories.bank_payments.bank_payment_repository import BankPaymentRepository


class BankPaymentService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = BankPaymentRepository(session)

    async def list_payments(self) -> list[BankPayment]:
        return await self._rows.list_all()

    async def record_payment(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        sales_invoice_id: UUID,
        party_bank_account_id: UUID,
        source_ref: str,
    ) -> BankPayment:
        row = BankPayment(
            id=uuid4(),
            organization_id=organization_id,
            sales_invoice_id=require_payment_invoice_id(sales_invoice_id),
            party_bank_account_id=require_payment_account_id(party_bank_account_id),
            source_ref=require_payment_source_ref(source_ref),
            created_by=user_id,
        )
        try:
            return await self._rows.add(row)
        except IntegrityError as orig:
            raise InvalidBankPayment("para już zapisana") from orig
