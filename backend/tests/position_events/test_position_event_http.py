from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.position_event import parse_position_event_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.position_event import PositionEvent
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "lat", "lng")


def test_migration_362_creates_position_event_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/362_position_event.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "362_position_event"' in source
    assert 'down_revision: str | None = "361_crm_opportunity"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "position_event_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency"):
        assert banned not in source


def test_importlinter_lists_position_event_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.position_events" in forbidden
    assert "app.models.position_event" in forbidden


def test_fga_source_declares_position_event_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_position_events: member" in source


def test_authorization_model_grants_position_events_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_position_events"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitPositionAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryPositionDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[PositionEvent] = []

    async def list_events(self) -> list[PositionEvent]:
        return list(self.rows)

    async def persist_position_event(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        event_code: object,
        source_kind: object,
        source_ref: object,
    ) -> PositionEvent:
        code, kind, origin = parse_position_event_row(
            event_code,
            source_kind,
            source_ref,
        )
        row = PositionEvent(
            id=uuid4(),
            organization_id=organization_id,
            event_code=code,
            source_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def position_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryPositionDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.position_events.PositionEventService",
        lambda _s: desk,
    )
    set_authz_checker(PermitPositionAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "event_code": "pos_yard_01",
        "source_kind": "gps",
        "source_ref": "fixture://position-event/a",
    }
    body.update(extra)
    return body


def test_post_position_event_persists(position_http: object) -> None:
    client, desk = position_http
    response = client.post(
        "/api/v1/position-events",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["source_kind"] == "gps"
    assert len(desk.rows) == 1


def test_post_position_event_rejects_amount_coords(position_http: object) -> None:
    client, _desk = position_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/position-events",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_position_event_rejects_bad_kind(position_http: object) -> None:
    client, _desk = position_http
    response = client.post(
        "/api/v1/position-events",
        headers=bearer_auth_headers(),
        json=_payload(source_kind="poll"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_position_event_rejects_foreign_source_ref(
    position_http: object,
) -> None:
    client, _desk = position_http
    response = client.post(
        "/api/v1/position-events",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_position_events_lists_rows(position_http: object) -> None:
    client, desk = position_http
    client.post(
        "/api/v1/position-events",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/position-events",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
