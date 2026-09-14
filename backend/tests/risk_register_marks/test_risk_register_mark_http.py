from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.risk_register_mark import parse_risk_register_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.risk_register_mark import RiskRegisterMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount",)


def test_migration_383_creates_risk_register_mark_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/386_risk_register_mark.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "386_risk_register_mark"' in source
    assert 'down_revision: str | None = "385_product_ticket_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "risk_register_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "score_person"):
        assert banned not in source


def test_importlinter_lists_risk_register_mark_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.risk_register_marks" in forbidden
    assert "app.models.risk_register_mark" in forbidden


def test_fga_source_declares_risk_register_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_risk_register_marks: member" in source


def test_authorization_model_grants_risk_register_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_risk_register_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class RiskRegisterMarkAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryLineImpactLayerDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[RiskRegisterMark] = []

    async def list_marks(self) -> list[RiskRegisterMark]:
        return list(self.rows)

    async def persist_risk_register_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        risk_kind: object,
        source_ref: object,
    ) -> RiskRegisterMark:
        code, kind, origin = parse_risk_register_mark_row(
            mark_code,
            risk_kind,
            source_ref,
        )
        row = RiskRegisterMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            risk_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def ops_room_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryLineImpactLayerDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.risk_register_marks.RiskRegisterMarkService",
        lambda _s: desk,
    )
    set_authz_checker(RiskRegisterMarkAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "rr_open_01",
        "risk_kind": "open",
        "source_ref": "fixture://risk-register/a",
    }
    body.update(extra)
    return body


def test_post_risk_register_mark_persists(ops_room_http: object) -> None:
    client, desk = ops_room_http
    response = client.post(
        "/api/v1/risk-register-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["risk_kind"] == "open"
    assert len(desk.rows) == 1


def test_post_risk_register_mark_rejects_amount(ops_room_http: object) -> None:
    client, _desk = ops_room_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/risk-register-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_risk_register_mark_rejects_bad_kind(ops_room_http: object) -> None:
    client, _desk = ops_room_http
    response = client.post(
        "/api/v1/risk-register-marks",
        headers=bearer_auth_headers(),
        json=_payload(risk_kind="score_person"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_risk_register_mark_rejects_foreign_source_ref(ops_room_http: object) -> None:
    client, _desk = ops_room_http
    response = client.post(
        "/api/v1/risk-register-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_risk_register_marks_lists_rows(ops_room_http: object) -> None:
    client, desk = ops_room_http
    client.post(
        "/api/v1/risk-register-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/risk-register-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
