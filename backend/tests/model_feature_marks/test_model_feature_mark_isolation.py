from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.database import bind_tenant
from app.models.model_feature_mark import ModelFeatureMark


def _row(
    *,
    organization_id,
    created_by,
    mark_code: str = "mf_numeric_01",
    feature_kind: str = "numeric",
    source_ref: str = "tenant:manual",
) -> ModelFeatureMark:
    return ModelFeatureMark(
        id=uuid4(),
        organization_id=organization_id,
        mark_code=mark_code,
        feature_kind=feature_kind,
        source_ref=source_ref,
        created_by=created_by,
    )


@pytest.mark.integration
@pytest.mark.asyncio
async def test_model_feature_mark_rls_isolates_tenants(
    session,
    two_tenants,
) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    row_a = _row(organization_id=org_a.id, created_by=user_a.id)
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    row_b = _row(
        organization_id=org_b.id,
        created_by=user_b.id,
        mark_code="mf_categorical_02",
        feature_kind="categorical",
        source_ref="fixture://model-feature-mark/b",
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(ModelFeatureMark))).all())
    assert {row.id for row in visible_a} == {row_a.id}

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(ModelFeatureMark))).all())
    assert {row.id for row in visible_b} == {row_b.id}
