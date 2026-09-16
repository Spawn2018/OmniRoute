from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.margin_floor import parse_margin_floor_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.margin_floor import MarginFloor
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]


def test_migration_417_creates_margin_floor_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/417_margin_floor.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "417_margin_floor"' in source
    assert 'down_revision: str | None = "416_kpi_definition_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "margin_floor_tenant_isolation" in source
    assert "floor_amount" in source
    assert "Numeric(14, 4)" in source
    for banned in ("float(", "httpx", "409", "sell-buy"):
        assert banned not in source


def test_importlinter_lists_margin_floor_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.margin_floors" in forbidden
    assert "app.models.margin_floor" in forbidden


def test_fga_source_declares_margin_floor_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_margin_floors: member" in source


def test_authorization_model_grants_margin_floors_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_margin_floors"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class MarginFloorAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryMarginFloorDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[MarginFloor] = []

    async def list_rows(self) -> list[MarginFloor]:
        return list(self.rows)

    async def persist_floor(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        floor_code: object,
        origin_unlocode: object,
        destination_unlocode: object,
        floor_amount: object,
        floor_currency: object,
        source_ref: object,
    ) -> MarginFloor:
        draft = parse_margin_floor_row(
            floor_code,
            origin_unlocode,
            destination_unlocode,
            floor_amount,
            floor_currency,
            source_ref,
        )
        row = MarginFloor(
            id=uuid4(),
            organization_id=organization_id,
            floor_code=draft.floor_code,
            origin_unlocode=draft.origin_unlocode,
            destination_unlocode=draft.destination_unlocode,
            floor_amount=draft.floor_amount,
            floor_currency=draft.floor_currency,
            source_ref=draft.source_ref,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def margin_floor_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryMarginFloorDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.margin_floors.MarginFloorService",
        lambda _s: desk,
    )
    set_authz_checker(MarginFloorAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "floor_code": "floor_gdn_ham",
        "origin_unlocode": "PLGDN",
        "destination_unlocode": "DEHAM",
        "floor_amount": "120",
        "floor_currency": "EUR",
        "source_ref": "fixture://margin-floor/a",
    }
    body.update(extra)
    return body


def test_post_margin_floor_persists(margin_floor_http: object) -> None:
    client, desk = margin_floor_http
    response = client.post(
        "/api/v1/margin-floors",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["floor_currency"] == "EUR"
    assert len(desk.rows) == 1


def test_post_margin_floor_rejects_numeric_amount(margin_floor_http: object) -> None:
    client, _desk = margin_floor_http
    response = client.post(
        "/api/v1/margin-floors",
        headers=bearer_auth_headers(),
        json=_payload(floor_amount=1.5),
    )
    assert response.status_code == 422


def test_post_margin_floor_rejects_bad_unlocode(margin_floor_http: object) -> None:
    client, _desk = margin_floor_http
    response = client.post(
        "/api/v1/margin-floors",
        headers=bearer_auth_headers(),
        json=_payload(origin_unlocode="PL@@@"),
    )
    assert response.status_code == 400
    assert "para miejsc" in response.json()["detail"]


def test_post_margin_floor_rejects_foreign_source_ref(margin_floor_http: object) -> None:
    client, _desk = margin_floor_http
    response = client.post(
        "/api/v1/margin-floors",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_margin_floors_lists_rows(margin_floor_http: object) -> None:
    client, desk = margin_floor_http
    client.post(
        "/api/v1/margin-floors",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/margin-floors",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
