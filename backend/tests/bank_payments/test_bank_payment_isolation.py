from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.bank_payment import BankPayment
from app.models.party_bank_account import PartyBankAccount
from app.models.sales_invoice import SalesInvoice
from tests.sales_invoices.test_sales_invoice_isolation import _booked


async def _invoice(session, *, ship, user_id, suffix: str) -> SalesInvoice:
    row = SalesInvoice(
        id=uuid4(),
        organization_id=ship.organization_id,
        shipment_id=ship.id,
        invoice_kind="issued",
        invoice_ref=f"FV/{suffix}",
        source_ref=f"fixture://sales-invoice/{suffix}",
        created_by=user_id,
    )
    session.add(row)
    await session.flush()
    return row


async def _account(session, *, ship, suffix: str) -> PartyBankAccount:
    row = PartyBankAccount(
        id=uuid4(),
        organization_id=ship.organization_id,
        party_id=ship.party_id,
        iban=f"PL61109010140000071219812{suffix[-2:]}",
        currency="PLN",
        whitelist_status="pending",
    )
    session.add(row)
    await session.flush()
    return row


async def _payment(session, *, org_id, user_id, invoice_id, account_id, suffix: str) -> BankPayment:
    row = BankPayment(
        id=uuid4(),
        organization_id=org_id,
        sales_invoice_id=invoice_id,
        party_bank_account_id=account_id,
        source_ref=f"fixture://bank-payment/{suffix}",
        created_by=user_id,
    )
    session.add(row)
    await session.flush()
    return row


@pytest.mark.integration
@pytest.mark.asyncio
async def test_bank_payment_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="pa")
    inv_a = await _invoice(session, ship=ship_a, user_id=user_a.id, suffix="pa")
    acc_a = await _account(session, ship=ship_a, suffix="pa")
    row_a = await _payment(
        session,
        org_id=org_a.id,
        user_id=user_a.id,
        invoice_id=inv_a.id,
        account_id=acc_a.id,
        suffix="a",
    )

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="pb")
    inv_b = await _invoice(session, ship=ship_b, user_id=user_b.id, suffix="pb")
    acc_b = await _account(session, ship=ship_b, suffix="pb")
    row_b = await _payment(
        session,
        org_id=org_b.id,
        user_id=user_b.id,
        invoice_id=inv_b.id,
        account_id=acc_b.id,
        suffix="b",
    )

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(BankPayment))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    foreign_b = await session.scalar(select(BankPayment).where(BankPayment.id == row_b.id))
    assert foreign_b is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(BankPayment))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_bank_payment_rejects_foreign_account(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    ship_b = await _booked(session, organization_id=org_b.id, user_id=user_b.id, suffix="xb")
    acc_b = await _account(session, ship=ship_b, suffix="xb")

    await bind_tenant(session, org_a.id)
    ship_a = await _booked(session, organization_id=org_a.id, user_id=user_a.id, suffix="xa")
    inv_a = await _invoice(session, ship=ship_a, user_id=user_a.id, suffix="xa")
    stolen = BankPayment(
        id=uuid4(),
        organization_id=org_a.id,
        sales_invoice_id=inv_a.id,
        party_bank_account_id=acc_b.id,
        source_ref="fixture://bank-payment/stolen",
        created_by=user_a.id,
    )
    session.add(stolen)
    with pytest.raises(IntegrityError):
        await session.flush()
