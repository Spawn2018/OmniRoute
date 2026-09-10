from datetime import time
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.terminal_slot_connector import (
    require_connector_code,
    require_cutoff_clock,
    require_gate_clock,
    require_slot_mode,
    require_slot_source_ref,
    require_terminal_code,
)
from app.main import app
from app.models.terminal_slot_connector import TerminalSlotConnector
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


class StubSlotDesk:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[TerminalSlotConnector] = []

    async def list_rows(self) -> list[TerminalSlotConnector]:
        return list(self.rows)

    async def persist_terminal_slot_connector(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        connector_code: object,
        terminal_code: object,
        mode: object,
        opens_local: object,
        closes_local: object,
        cutoff_local: object,
        source_ref: object,
    ) -> TerminalSlotConnector:
        row = TerminalSlotConnector(
            id=uuid4(),
            organization_id=organization_id,
            connector_code=require_connector_code(connector_code),
            terminal_code=require_terminal_code(terminal_code),
            mode=require_slot_mode(mode),
            opens_local=require_gate_clock(opens_local),
            closes_local=require_gate_clock(closes_local),
            cutoff_local=require_cutoff_clock(cutoff_local),
            source_ref=require_slot_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = StubSlotDesk(object())

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.terminal_slot_connectors.TerminalSlotConnectorService",
        lambda _s: desk,
    )
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "connector_code": "gdynia_bct",
        "terminal_code": "plgdy_bct",
        "mode": "email_hitl",
        "opens_local": "06:00",
        "closes_local": "22:00",
        "cutoff_local": "16:00",
        "source_ref": "fixture://terminal-slot-connector/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_slot_connector(catalog_client: object) -> None:
    client, _desk = catalog_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post("/api/v1/terminal-slot-connectors", headers=headers, json=_payload())
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["connector_code"] == "gdynia_bct"
    assert body["terminal_code"] == "plgdy_bct"
    assert body["mode"] == "email_hitl"
    assert body["opens_local"] == "06:00:00"
    assert "confirmed" not in body
    assert "buy_amount" not in body
    assert "margin" not in body
    listed = client.get("/api/v1/terminal-slot-connectors", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_rejects_confirmed_in_body(catalog_client: object) -> None:
    client, desk = catalog_client
    response = client.post(
        "/api/v1/terminal-slot-connectors",
        headers=bearer_auth_headers(),
        json=_payload(confirmed=True),
    )
    assert response.status_code == 422
    assert desk.rows == []


def test_http_create_bad_code_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/terminal-slot-connectors",
        headers=bearer_auth_headers(),
        json=_payload(connector_code="X"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_http_create_bad_terminal_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/terminal-slot-connectors",
        headers=bearer_auth_headers(),
        json=_payload(terminal_code="BCT"),
    )
    assert response.status_code == 400
    assert "terminal" in response.json()["detail"]


def test_http_create_navis_mode_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/terminal-slot-connectors",
        headers=bearer_auth_headers(),
        json=_payload(mode="navis"),
    )
    assert response.status_code == 400
    assert "tryb" in response.json()["detail"]


def test_http_create_bad_hours_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/terminal-slot-connectors",
        headers=bearer_auth_headers(),
        json=_payload(opens_local="25:00"),
    )
    assert response.status_code == 400
    assert "godziny" in response.json()["detail"]


def test_http_create_bad_cutoff_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/terminal-slot-connectors",
        headers=bearer_auth_headers(),
        json=_payload(cutoff_local="night"),
    )
    assert response.status_code == 400
    assert "odcięcie" in response.json()["detail"]


def test_http_create_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/terminal-slot-connectors",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://n4.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]


def test_http_create_overnight_hours_are_legal(catalog_client: object) -> None:
    client, _desk = catalog_client
    response = client.post(
        "/api/v1/terminal-slot-connectors",
        headers=bearer_auth_headers(),
        json=_payload(opens_local="22:00", closes_local="06:00"),
    )
    assert response.status_code == 201
    assert response.json()["opens_local"] == "22:00:00"
    assert time.fromisoformat(response.json()["closes_local"]) == time(6, 0)
