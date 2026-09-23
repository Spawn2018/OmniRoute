from decimal import Decimal
from uuid import UUID, uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.charge_code import ChargeCode
from app.models.port import Port
from tests.parties._load import load_attr

_MANUAL = "tenant:manual"
_UNLOCODE_SOURCE = "github:cristan/improved-un-locodes@fixture"


def _party_cls():
    return load_attr("app.models.party", "Party")


def _assignment_cls():
    return load_attr("app.models.party_role_assignment", "PartyRoleAssignment")


def _contact_cls():
    return load_attr("app.models.party_contact", "PartyContact")


def _bank_cls():
    return load_attr("app.models.party_bank_account", "PartyBankAccount")


def _domain_cls():
    return load_attr("app.models.party_email_domain", "PartyEmailDomain")


def _override_cls():
    return load_attr("app.models.party_charge_override", "PartyChargeOverride")


def _carrier_cls():
    return load_attr("app.models.carrier_profile", "CarrierProfile")


def _terminal_cls():
    return load_attr("app.models.terminal", "Terminal")


def _party(
    *,
    organization_id: UUID,
    legal_name: str,
    tax_id: str | None = None,
    vat_eu: str | None = None,
    eori: str | None = None,
    duns: str | None = None,
    country_code: str = "PL",
    created_by: UUID | None = None,
    credit_limit: Decimal | None = None,
    credit_currency: str | None = None,
    roles: list[str] | None = None,
):
    return _party_cls()(
        id=uuid4(),
        organization_id=organization_id,
        legal_name=legal_name,
        country_code=country_code,
        tax_id=tax_id,
        vat_eu=vat_eu,
        eori=eori,
        duns=duns,
        roles=roles or ["customer"],
        credit_limit=credit_limit,
        credit_currency=credit_currency,
        source_ref=_MANUAL,
        is_active=True,
        created_by=created_by,
    )


def _port(*, organization_id: UUID, unlocode: str) -> Port:
    return Port(
        id=uuid4(),
        organization_id=organization_id,
        unlocode=unlocode,
        name=unlocode,
        country_code=unlocode[:2],
        is_seaport=True,
        function_flags=["port"],
        aliases=[],
        is_official=True,
        source_ref=_UNLOCODE_SOURCE,
    )


async def _flush_party(session, two_tenants, org_key: str, **kwargs):
    org = two_tenants[org_key]
    user = two_tenants["user_a" if org_key == "org_a" else "user_b"]
    await bind_tenant(session, org.id)
    row = _party(organization_id=org.id, created_by=user.id, **kwargs)
    session.add(row)
    await session.flush()
    return row


async def _assert_isolated(session, two_tenants, model, row_a, row_b) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(model))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(select(model).where(model.id == row_b.id)) is None
    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(model))).all())
    assert {row.id for row in visible_b} == {row_b.id}
    assert await session.scalar(select(model).where(model.id == row_a.id)) is None


@pytest.mark.integration
@pytest.mark.asyncio
async def test_party_rls_isolates_tenants(session, two_tenants) -> None:
    party_a = await _flush_party(session, two_tenants, "org_a", legal_name="ACME A")
    party_b = await _flush_party(session, two_tenants, "org_b", legal_name="ACME B")
    await _assert_isolated(session, two_tenants, _party_cls(), party_a, party_b)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_party_contact_rls_isolates_tenants(session, two_tenants) -> None:
    Contact = _contact_cls()
    party_a = await _flush_party(session, two_tenants, "org_a", legal_name="ACME A")
    party_b = await _flush_party(session, two_tenants, "org_b", legal_name="ACME B")
    await bind_tenant(session, two_tenants["org_a"].id)
    contact_a = Contact(
        id=uuid4(),
        organization_id=two_tenants["org_a"].id,
        party_id=party_a.id,
        name="Anna A",
        is_primary=True,
    )
    session.add(contact_a)
    await session.flush()
    await bind_tenant(session, two_tenants["org_b"].id)
    contact_b = Contact(
        id=uuid4(),
        organization_id=two_tenants["org_b"].id,
        party_id=party_b.id,
        name="Bartek B",
        is_primary=True,
    )
    session.add(contact_b)
    await session.flush()
    await _assert_isolated(session, two_tenants, Contact, contact_a, contact_b)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_party_bank_account_rls_isolates_tenants(session, two_tenants) -> None:
    Bank = _bank_cls()
    party_a = await _flush_party(session, two_tenants, "org_a", legal_name="ACME A")
    party_b = await _flush_party(session, two_tenants, "org_b", legal_name="ACME B")
    await bind_tenant(session, two_tenants["org_a"].id)
    bank_a = Bank(
        id=uuid4(),
        organization_id=two_tenants["org_a"].id,
        party_id=party_a.id,
        iban="PL61109010140000071219812874",
        currency="PLN",
        whitelist_status="pending",
    )
    session.add(bank_a)
    await session.flush()
    await bind_tenant(session, two_tenants["org_b"].id)
    bank_b = Bank(
        id=uuid4(),
        organization_id=two_tenants["org_b"].id,
        party_id=party_b.id,
        iban="DE89370400440532013000",
        currency="EUR",
        whitelist_status="pending",
    )
    session.add(bank_b)
    await session.flush()
    await _assert_isolated(session, two_tenants, Bank, bank_a, bank_b)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_party_email_domain_rls_isolates_tenants(session, two_tenants) -> None:
    Domain = _domain_cls()
    party_a = await _flush_party(session, two_tenants, "org_a", legal_name="ACME A")
    party_b = await _flush_party(session, two_tenants, "org_b", legal_name="ACME B")
    await bind_tenant(session, two_tenants["org_a"].id)
    domain_a = Domain(
        id=uuid4(),
        organization_id=two_tenants["org_a"].id,
        party_id=party_a.id,
        domain="acme-a.pl",
        source_ref=_MANUAL,
    )
    session.add(domain_a)
    await session.flush()
    await bind_tenant(session, two_tenants["org_b"].id)
    domain_b = Domain(
        id=uuid4(),
        organization_id=two_tenants["org_b"].id,
        party_id=party_b.id,
        domain="acme-b.de",
        source_ref=_MANUAL,
    )
    session.add(domain_b)
    await session.flush()
    await _assert_isolated(session, two_tenants, Domain, domain_a, domain_b)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_party_charge_override_rls_isolates_tenants(session, two_tenants) -> None:
    Override = _override_cls()
    party_a = await _flush_party(session, two_tenants, "org_a", legal_name="ACME A")
    party_b = await _flush_party(session, two_tenants, "org_b", legal_name="ACME B")
    await bind_tenant(session, two_tenants["org_a"].id)
    session.add(
        ChargeCode(
            id=uuid4(),
            organization_id=two_tenants["org_a"].id,
            code="THC",
            name="Terminal",
            aliases=[],
        )
    )
    await session.flush()
    override_a = Override(
        id=uuid4(),
        organization_id=two_tenants["org_a"].id,
        party_id=party_a.id,
        charge_code="THC",
        amount=Decimal("15.0000"),
        currency="USD",
        source_ref=_MANUAL,
    )
    session.add(override_a)
    await session.flush()
    await bind_tenant(session, two_tenants["org_b"].id)
    session.add(
        ChargeCode(
            id=uuid4(),
            organization_id=two_tenants["org_b"].id,
            code="THC",
            name="Terminal",
            aliases=[],
        )
    )
    await session.flush()
    override_b = Override(
        id=uuid4(),
        organization_id=two_tenants["org_b"].id,
        party_id=party_b.id,
        charge_code="THC",
        amount=Decimal("20.0000"),
        currency="EUR",
        source_ref=_MANUAL,
    )
    session.add(override_b)
    await session.flush()
    await _assert_isolated(session, two_tenants, Override, override_a, override_b)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_carrier_profile_rls_isolates_tenants(session, two_tenants) -> None:
    Carrier = _carrier_cls()
    party_a = await _flush_party(session, two_tenants, "org_a", legal_name="ACME A")
    party_b = await _flush_party(session, two_tenants, "org_b", legal_name="ACME B")
    await bind_tenant(session, two_tenants["org_a"].id)
    profile_a = Carrier(
        id=uuid4(),
        organization_id=two_tenants["org_a"].id,
        party_id=party_a.id,
        is_nvocc=False,
        api_adapter="none",
    )
    session.add(profile_a)
    await session.flush()
    await bind_tenant(session, two_tenants["org_b"].id)
    profile_b = Carrier(
        id=uuid4(),
        organization_id=two_tenants["org_b"].id,
        party_id=party_b.id,
        is_nvocc=True,
        api_adapter="maersk",
    )
    session.add(profile_b)
    await session.flush()
    await _assert_isolated(session, two_tenants, Carrier, profile_a, profile_b)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_party_contact_may_not_point_at_another_tenant_party(session, two_tenants) -> None:
    party_a = await _flush_party(session, two_tenants, "org_a", legal_name="ACME A")
    await bind_tenant(session, two_tenants["org_b"].id)
    session.add(
        _contact_cls()(
            id=uuid4(),
            organization_id=two_tenants["org_b"].id,
            party_id=party_a.id,
            name="Obcy kontakt",
            is_primary=False,
        )
    )
    with pytest.raises(IntegrityError, match="fk_party_contact_party"):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_party_charge_override_may_not_use_another_tenant_charge_code(
    session,
    two_tenants,
) -> None:
    party_a = await _flush_party(session, two_tenants, "org_a", legal_name="ACME A")
    await bind_tenant(session, two_tenants["org_b"].id)
    session.add(
        ChargeCode(
            id=uuid4(),
            organization_id=two_tenants["org_b"].id,
            code="BAF",
            name="Bunker",
            aliases=[],
        )
    )
    await session.flush()
    await bind_tenant(session, two_tenants["org_a"].id)
    session.add(
        _override_cls()(
            id=uuid4(),
            organization_id=two_tenants["org_a"].id,
            party_id=party_a.id,
            charge_code="BAF",
            amount=Decimal("1.0000"),
            currency="USD",
            source_ref=_MANUAL,
        )
    )
    with pytest.raises(IntegrityError, match="fk_party_charge_override_charge_code"):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_terminal_may_not_point_operator_at_another_tenant_party(
    session,
    two_tenants,
) -> None:
    assert "operator_party_id" in _terminal_cls().__table__.c
    party_a = await _flush_party(session, two_tenants, "org_a", legal_name="BCT")
    await bind_tenant(session, two_tenants["org_b"].id)
    port_b = _port(organization_id=two_tenants["org_b"].id, unlocode="DEHAM")
    session.add(port_b)
    await session.flush()
    session.add(
        _terminal_cls()(
            id=uuid4(),
            organization_id=two_tenants["org_b"].id,
            port_id=port_b.id,
            name="HHLA",
            operator_name="HHLA",
            operator_party_id=party_a.id,
            source_ref=_MANUAL,
        )
    )
    with pytest.raises(IntegrityError, match="fk_terminal_operator_party"):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_tax_id_is_unique_inside_one_tenant_country(session, two_tenants) -> None:
    await _flush_party(
        session,
        two_tenants,
        "org_a",
        legal_name="ACME 1",
        tax_id="1234563218",
    )
    session.add(
        _party(
            organization_id=two_tenants["org_a"].id,
            legal_name="ACME 2",
            tax_id="1234563218",
        )
    )
    with pytest.raises(IntegrityError, match="uq_party_org_country_tax_id"):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_role_assignment_rls_isolates_tenants(session, two_tenants) -> None:
    Assignment = _assignment_cls()
    party_a = await _flush_party(
        session, two_tenants, "org_a", legal_name="ACME A", roles=["vendor"],
    )
    party_b = await _flush_party(
        session, two_tenants, "org_b", legal_name="ACME B", roles=["vendor"],
    )
    await bind_tenant(session, two_tenants["org_a"].id)
    row_a = Assignment(
        id=uuid4(),
        organization_id=two_tenants["org_a"].id,
        party_id=party_a.id,
        role="vendor",
        source_ref=_MANUAL,
    )
    session.add(row_a)
    await session.flush()
    await bind_tenant(session, two_tenants["org_b"].id)
    row_b = Assignment(
        id=uuid4(),
        organization_id=two_tenants["org_b"].id,
        party_id=party_b.id,
        role="vendor",
        source_ref=_MANUAL,
    )
    session.add(row_b)
    await session.flush()
    await _assert_isolated(session, two_tenants, Assignment, row_a, row_b)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_eori_is_unique_inside_one_tenant(session, two_tenants) -> None:
    await _flush_party(
        session,
        two_tenants,
        "org_a",
        legal_name="ACME 1",
        eori="PL1234563218000",
        roles=["vendor"],
    )
    session.add(
        _party(
            organization_id=two_tenants["org_a"].id,
            legal_name="ACME 2",
            eori="PL1234563218000",
            roles=["vendor"],
        )
    )
    with pytest.raises(IntegrityError, match="uq_party_org_eori"):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_two_tenants_may_hold_the_same_eori(session, two_tenants) -> None:
    await _flush_party(
        session,
        two_tenants,
        "org_a",
        legal_name="ACME A",
        eori="PL1234563218000",
        roles=["vendor"],
    )
    await _flush_party(
        session,
        two_tenants,
        "org_b",
        legal_name="ACME B",
        eori="PL1234563218000",
        roles=["vendor"],
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_two_tenants_may_hold_the_same_tax_id(session, two_tenants) -> None:
    await _flush_party(
        session,
        two_tenants,
        "org_a",
        legal_name="ACME A",
        tax_id="1234563218",
    )
    await _flush_party(
        session,
        two_tenants,
        "org_b",
        legal_name="ACME B",
        tax_id="1234563218",
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_credit_limit_without_currency_is_rejected_by_the_database(
    session,
    two_tenants,
) -> None:
    await bind_tenant(session, two_tenants["org_a"].id)
    session.add(
        _party(
            organization_id=two_tenants["org_a"].id,
            legal_name="ACME",
            credit_limit=Decimal("1000.0000"),
            credit_currency=None,
        )
    )
    with pytest.raises(IntegrityError, match="ck_party_credit_pair"):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_role_outside_allowlist_is_rejected_by_the_database(session, two_tenants) -> None:
    await bind_tenant(session, two_tenants["org_a"].id)
    session.add(
        _party(
            organization_id=two_tenants["org_a"].id,
            legal_name="ACME",
            roles=["client"],
        )
    )
    with pytest.raises(IntegrityError, match="ck_party_roles"):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_party_without_tenant_context_is_invisible(session, two_tenants) -> None:
    Party = _party_cls()
    await _flush_party(session, two_tenants, "org_a", legal_name="ACME")
    session.expunge_all()
    await session.execute(text("SELECT set_config('app.current_org', '', true)"))
    assert list((await session.scalars(select(Party))).all()) == []


def test_party_organization_id_rejects_null() -> None:
    column = _party_cls().__table__.c.organization_id
    assert column.nullable is False


def test_party_contact_has_no_portal_columns() -> None:
    columns = set(_contact_cls().__table__.c.keys())
    assert "portal_user_id" not in columns
    assert "portal_access" not in columns


def test_party_contact_has_tracking_consent_bool() -> None:
    column = _contact_cls().__table__.c.tracking_consent
    assert column.nullable is False
    assert column.type.python_type is bool


def test_terminal_operator_party_id_is_nullable() -> None:
    columns = _terminal_cls().__table__.c
    assert "operator_party_id" in columns
    assert columns["operator_party_id"].nullable is True
