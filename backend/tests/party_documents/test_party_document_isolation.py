from uuid import uuid4

import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from app.core.database import bind_tenant
from app.models.party import Party
from app.models.party_document import PartyDocument


def _party(*, organization_id, legal_name: str, created_by) -> Party:
    return Party(
        id=uuid4(),
        organization_id=organization_id,
        legal_name=legal_name,
        country_code="PL",
        roles=["carrier"],
        source_ref="tenant:manual",
        is_active=True,
        created_by=created_by,
    )


def _document(
    *,
    organization_id,
    created_by,
    party_id,
    document_kind: str = "ocp",
) -> PartyDocument:
    return PartyDocument(
        id=uuid4(),
        organization_id=organization_id,
        party_id=party_id,
        document_kind=document_kind,
        source_ref="tenant:manual",
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_party_document_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    firm_a = _party(organization_id=org_a.id, legal_name="Haulier A", created_by=user_a.id)
    session.add(firm_a)
    await session.flush()
    row_a = _document(organization_id=org_a.id, created_by=user_a.id, party_id=firm_a.id)
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    firm_b = _party(organization_id=org_b.id, legal_name="Haulier B", created_by=user_b.id)
    session.add(firm_b)
    await session.flush()
    row_b = _document(
        organization_id=org_b.id,
        created_by=user_b.id,
        party_id=firm_b.id,
        document_kind="ocs",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(PartyDocument))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(select(PartyDocument).where(PartyDocument.id == row_b.id)) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(PartyDocument))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_party_document_rejects_foreign_party(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_b.id)
    party_b = _party(organization_id=org_b.id, legal_name="Haulier X", created_by=user_b.id)
    session.add(party_b)
    await session.flush()

    await bind_tenant(session, org_a.id)
    session.add(
        _document(
            organization_id=org_a.id,
            created_by=user_a.id,
            party_id=party_b.id,
        ),
    )
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_party_document_rejects_duplicate_kind(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    firm_a = _party(organization_id=org_a.id, legal_name="Haulier A", created_by=user_a.id)
    session.add(firm_a)
    await session.flush()
    session.add(_document(organization_id=org_a.id, created_by=user_a.id, party_id=firm_a.id))
    await session.flush()
    session.add(_document(organization_id=org_a.id, created_by=user_a.id, party_id=firm_a.id))
    with pytest.raises(IntegrityError):
        await session.flush()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_party_document_list_uses_org_index(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    plan = await session.execute(
        text("EXPLAIN SELECT id FROM party_document WHERE organization_id = :org_id"),
        {"org_id": org_a.id},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert (
        "ix_party_document_organization_id" in joined
        or "uq_party_document_org_party_kind" in joined
    )
