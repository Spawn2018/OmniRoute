from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.customer_contract import (
    require_contract_code,
    require_contract_source_ref,
    require_shipper_label,
    require_their_customer_label,
    resolve_opaque_blob,
)
from app.models.customer_contract import CustomerContract
from app.repositories.customer_contracts.customer_contract_repository import (
    CustomerContractRepository,
)


class CustomerContractService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = CustomerContractRepository(session)

    async def list_rows(self) -> list[CustomerContract]:
        return await self._rows.fetch_rows()

    async def persist_customer_contract(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        contract_code: object,
        shipper_label: object,
        their_customer_label: object,
        source_ref: object,
        opaque_fixture: object = False,
        opaque_blob: object = None,
    ) -> CustomerContract:
        row = CustomerContract(
            id=uuid4(),
            organization_id=organization_id,
            contract_code=require_contract_code(contract_code),
            shipper_label=require_shipper_label(shipper_label),
            their_customer_label=require_their_customer_label(their_customer_label),
            source_ref=require_contract_source_ref(source_ref),
            blob_ciphertext=resolve_opaque_blob(
                opaque_fixture=opaque_fixture,
                opaque_blob=opaque_blob,
            ),
            created_by=user_id,
        )
        return await self._rows.add(row)
