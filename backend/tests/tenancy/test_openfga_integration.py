import os
from uuid import uuid4

import pytest

from app.integrations.openfga.client import OpenFgaAuthz, bootstrap_store, build_openfga_client

OPENFGA_API_URL = os.getenv("OPENFGA_API_URL", "http://localhost:8080")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_openfga_member_can_list_users(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENFGA_API_URL", OPENFGA_API_URL)
    monkeypatch.setattr(
        "app.core.config.settings.openfga_api_url",
        OPENFGA_API_URL,
    )
    monkeypatch.setattr("app.core.config.settings.openfga_store_id", "")
    monkeypatch.setattr("app.core.config.settings.openfga_model_id", "")

    client = await build_openfga_client()
    try:
        await bootstrap_store(client, store_name=f"test-{uuid4().hex[:8]}")
        authz = OpenFgaAuthz(client)

        org_id = uuid4()
        member_id = uuid4()
        stranger_id = uuid4()

        await authz.write_member(user_id=member_id, organization_id=org_id)

        assert await authz.check(
            user_id=member_id,
            relation="can_list_users",
            object_type="organization",
            object_id=org_id,
        )
        assert not await authz.check(
            user_id=stranger_id,
            relation="can_list_users",
            object_type="organization",
            object_id=org_id,
        )
        assert not await authz.check(
            user_id=member_id,
            relation="can_review_extractions",
            object_type="organization",
            object_id=org_id,
        )
        reviewer_id = uuid4()
        await authz.write_reviewer(user_id=reviewer_id, organization_id=org_id)
        assert await authz.check(
            user_id=reviewer_id,
            relation="can_review_extractions",
            object_type="organization",
            object_id=org_id,
        )
    finally:
        await client.close()
