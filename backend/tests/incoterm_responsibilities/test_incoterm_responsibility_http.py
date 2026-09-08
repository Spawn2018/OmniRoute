from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.incoterm_responsibility import (
    omni_ops_seed_pairs,
    require_booking_scope,
    require_clearance_role,
    require_main_carriage_booker,
    require_responsibility_incoterm,
    require_responsibility_source_ref,
    require_responsibility_trade_side,
)
from app.main import app
from app.models.incoterm_responsibility import IncotermResponsibility
from tests.http_auth import bearer_auth_headers


class AllowAllAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class StubIncotermResponsibilityService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[IncotermResponsibility] = []

    async def list_for_pair(
        self,
        *,
        incoterm: object,
        trade_side: object,
    ) -> list[IncotermResponsibility]:
        code = require_responsibility_incoterm(incoterm)
        side = require_responsibility_trade_side(trade_side)
        return [
            row
            for row in self.rows
            if str(row.incoterm).strip() == code
            and row.trade_side == side
            and row.superseded_by is None
        ]

    async def record_rule(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        incoterm: object,
        trade_side: object,
        export_clearance_role: object,
        import_clearance_role: object,
        main_carriage_booker: object,
        booking_scope: object,
        source_ref: object,
    ) -> IncotermResponsibility:
        code = require_responsibility_incoterm(incoterm)
        side = require_responsibility_trade_side(trade_side)
        export_role = require_clearance_role(
            export_clearance_role,
            field="export_clearance_role",
        )
        import_role = require_clearance_role(
            import_clearance_role,
            field="import_clearance_role",
        )
        booker = require_main_carriage_booker(main_carriage_booker)
        scope = require_booking_scope(booking_scope)
        origin = require_responsibility_source_ref(source_ref)
        current = next(
            (
                row
                for row in self.rows
                if str(row.incoterm).strip() == code
                and row.trade_side == side
                and row.superseded_by is None
            ),
            None,
        )
        if (
            current is not None
            and current.export_clearance_role == export_role
            and current.import_clearance_role == import_role
            and current.main_carriage_booker == booker
            and list(current.booking_scope) == scope
            and current.source_ref == origin
        ):
            return current
        successor = IncotermResponsibility(
            id=uuid4(),
            organization_id=organization_id,
            incoterm=code,
            trade_side=side,
            export_clearance_role=export_role,
            import_clearance_role=import_role,
            main_carriage_booker=booker,
            booking_scope=scope,
            source_ref=origin,
            created_by=user_id,
        )
        if current is not None:
            current.superseded_by = successor.id
        self.rows.append(successor)
        return successor

    async def seed_omni_ops(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
    ) -> list[IncotermResponsibility]:
        present = {
            (str(row.incoterm).strip(), row.trade_side)
            for row in self.rows
            if row.superseded_by is None
        }
        for pair in omni_ops_seed_pairs():
            key = (str(pair["incoterm"]), str(pair["trade_side"]))
            if key in present:
                continue
            await self.record_rule(
                organization_id=organization_id,
                user_id=user_id,
                incoterm=pair["incoterm"],
                trade_side=pair["trade_side"],
                export_clearance_role=pair["export_clearance_role"],
                import_clearance_role=pair["import_clearance_role"],
                main_carriage_booker=pair["main_carriage_booker"],
                booking_scope=pair["booking_scope"],
                source_ref=pair["source_ref"],
            )
            present.add(key)
        return [row for row in self.rows if row.superseded_by is None]


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    rules = StubIncotermResponsibilityService(object())

    def _rows(_session: object) -> StubIncotermResponsibilityService:
        return rules

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.incoterm_responsibilities.IncotermResponsibilityService",
        _rows,
    )
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), rules
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_seed_twenty_two_and_ddp_seller(catalog_client: object) -> None:
    client, _rules = catalog_client
    headers = bearer_auth_headers()
    seeded = client.post("/api/v1/incoterm-responsibilities/seed", headers=headers)
    assert seeded.status_code == 201
    body = seeded.json()
    assert len(body) == 22
    ddp = next(row for row in body if row["incoterm"] == "DDP" and row["trade_side"] == "import")
    assert ddp["import_clearance_role"] == "seller"
    assert "ICC" not in str(body)
    listed = client.get(
        "/api/v1/incoterm-responsibilities",
        headers=headers,
        params={"incoterm": "DDP", "trade_side": "import"},
    )
    assert listed.json()[0]["id"] == ddp["id"]
    again = client.post("/api/v1/incoterm-responsibilities/seed", headers=headers)
    assert again.status_code == 201
    assert len(again.json()) == 22


def test_http_override_supersedes_and_unknown_incoterm_is_400(catalog_client: object) -> None:
    client, _rules = catalog_client
    headers = bearer_auth_headers()
    first = client.post(
        "/api/v1/incoterm-responsibilities",
        headers=headers,
        json={
            "incoterm": "FOB",
            "trade_side": "export",
            "export_clearance_role": "seller",
            "import_clearance_role": "buyer",
            "main_carriage_booker": "buyer",
            "booking_scope": ["ocean"],
            "source_ref": "tenant:manual",
        },
    )
    first_id = first.json()["id"]
    second = client.post(
        "/api/v1/incoterm-responsibilities",
        headers=headers,
        json={
            "incoterm": "FOB",
            "trade_side": "export",
            "export_clearance_role": "omni_customs",
            "import_clearance_role": "buyer",
            "main_carriage_booker": "buyer",
            "booking_scope": ["ocean"],
            "source_ref": "tenant:manual",
        },
    )
    assert second.json()["id"] != first_id
    listed = client.get(
        "/api/v1/incoterm-responsibilities",
        headers=headers,
        params={"incoterm": "FOB", "trade_side": "export"},
    )
    assert listed.json()[0]["id"] == second.json()["id"]
    seeded = client.post("/api/v1/incoterm-responsibilities/seed", headers=headers)
    assert seeded.status_code == 201
    after_seed = client.get(
        "/api/v1/incoterm-responsibilities",
        headers=headers,
        params={"incoterm": "FOB", "trade_side": "export"},
    )
    assert after_seed.json()[0]["id"] == second.json()["id"]
    assert after_seed.json()[0]["export_clearance_role"] == "omni_customs"
    bad = client.post(
        "/api/v1/incoterm-responsibilities",
        headers=headers,
        json={
            "incoterm": "XXX",
            "trade_side": "export",
            "export_clearance_role": "seller",
            "import_clearance_role": "buyer",
            "main_carriage_booker": "buyer",
            "booking_scope": ["ocean"],
            "source_ref": "tenant:manual",
        },
    )
    assert bad.status_code == 400
