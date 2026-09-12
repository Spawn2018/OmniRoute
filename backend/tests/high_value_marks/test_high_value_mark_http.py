from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.high_value_mark import parse_high_value_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.high_value_mark import HighValueMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]

_FORBIDDEN = ("amount", "margin", "score", "cargo_value")


def test_migration_333_creates_high_value_and_rls() -> None:
    source = (
        _ROOT / "backend/alembic/versions/333_high_value_mark.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "333_high_value_mark"' in source
    assert 'down_revision: str | None = "332_profit_center_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "high_value_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency"):
        assert banned not in source.lower()
    assert 'sa.Column("amount"' not in source
    assert 'sa.Column("cargo_value"' not in source


def test_importlinter_lists_high_value_on_deny() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.high_value_marks" in forbidden
    assert "app.models.high_value_mark" in forbidden


def test_api_types_include_high_value_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "HighValueMarkResponse" in source
    assert "HighValueMarkCreate" in source


def test_fga_source_declares_high_value_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_high_value_marks: member" in source


def test_fga_model_grants_high_value_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_high_value_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitHighValueAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryHighValueDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[HighValueMark] = []

    async def list_marks(self) -> list[HighValueMark]:
        return list(self.rows)

    async def persist_high_value_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        protocol_kind: object,
        source_ref: object,
    ) -> HighValueMark:
        code, kind, origin = parse_high_value_mark_row(
            mark_code,
            protocol_kind,
            source_ref,
        )
        row = HighValueMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            protocol_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def high_value_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryHighValueDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.high_value_marks.HighValueMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitHighValueAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "hvm_high_value_01",
        "protocol_kind": "high_value",
        "source_ref": "fixture://high-value-mark/a",
    }
    body.update(extra)
    return body


def test_post_persists(high_value_http: object) -> None:
    client, desk = high_value_http
    response = client.post(
        "/api/v1/high-value-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["protocol_kind"] == "high_value"
    assert response.headers.get("X-Omni-Catalog") == "high-value-mark"
    assert len(desk.rows) == 1


def test_post_rejects_amount_margin_score_cargo_value(high_value_http: object) -> None:
    client, _desk = high_value_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/high-value-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_rejects_bad_code(high_value_http: object) -> None:
    client, _desk = high_value_http
    response = client.post(
        "/api/v1/high-value-marks",
        headers=bearer_auth_headers(),
        json=_payload(mark_code="BAD"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_post_rejects_bad_kind(high_value_http: object) -> None:
    client, _desk = high_value_http
    response = client.post(
        "/api/v1/high-value-marks",
        headers=bearer_auth_headers(),
        json=_payload(protocol_kind="insurance"),
    )
    assert response.status_code == 400
    assert "protoko" in response.json()["detail"]


def test_post_rejects_foreign_source_ref(high_value_http: object) -> None:
    client, _desk = high_value_http
    response = client.post(
        "/api/v1/high-value-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_lists_rows(high_value_http: object) -> None:
    client, desk = high_value_http
    client.post(
        "/api/v1/high-value-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/high-value-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
