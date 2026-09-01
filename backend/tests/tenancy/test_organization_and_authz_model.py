from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.integrations.openfga.model import authorization_model_request
from app.models.organization import Organization
from app.repositories.tenancy.organization_repository import OrganizationRepository


def test_authorization_model_includes_table_view_permission() -> None:
    request = authorization_model_request()
    org = next(td for td in request.type_definitions if td.type == "organization")
    assert "can_list_users" in org.relations
    assert "can_manage_table_views" in org.relations
    assert "can_review_extractions" in org.relations
    assert "can_manage_charge_codes" in org.relations
    assert "can_manage_commodity_codes" in org.relations
    assert "can_manage_nbp_rates" in org.relations
    assert "can_manage_rate_lines" in org.relations
    assert "can_manage_charges" in org.relations
    assert "can_manage_quotations" in org.relations
    assert "can_manage_organization_settings" in org.relations
    assert "member" in org.relations
    assert "reviewer" in org.relations
    review = org.relations["can_review_extractions"]
    assert review.computed_userset is not None
    assert review.computed_userset.relation == "reviewer"
    listing = org.relations["can_list_users"]
    assert listing.computed_userset is not None
    assert listing.computed_userset.relation == "member"
    catalog = org.relations["can_manage_charge_codes"]
    assert catalog.computed_userset is not None
    assert catalog.computed_userset.relation == "member"
    commodities = org.relations["can_manage_commodity_codes"]
    assert commodities.computed_userset is not None
    assert commodities.computed_userset.relation == "member"
    nbp = org.relations["can_manage_nbp_rates"]
    assert nbp.computed_userset is not None
    assert nbp.computed_userset.relation == "member"
    rates = org.relations["can_manage_rate_lines"]
    assert rates.computed_userset is not None
    assert rates.computed_userset.relation == "member"
    charges = org.relations["can_manage_charges"]
    assert charges.computed_userset is not None
    assert charges.computed_userset.relation == "member"
    quotations = org.relations["can_manage_quotations"]
    assert quotations.computed_userset is not None
    assert quotations.computed_userset.relation == "member"
    settings = org.relations["can_manage_organization_settings"]
    assert settings.computed_userset is not None
    assert settings.computed_userset.relation == "member"


@pytest.mark.asyncio
async def test_organization_repository_getters() -> None:
    session = AsyncMock()
    org = Organization(id=uuid4(), name="A", slug="a")
    session.get = AsyncMock(return_value=org)
    session.scalar = AsyncMock(return_value=org)
    repo = OrganizationRepository(session)

    assert await repo.get_by_id(org.id) is org
    assert await repo.get_by_slug("a") is org
    session.get.assert_awaited()
    session.scalar.assert_awaited()
