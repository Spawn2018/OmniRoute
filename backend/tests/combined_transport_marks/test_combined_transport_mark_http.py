from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.combined_transport_mark import parse_combined_transport_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.combined_transport_mark import CombinedTransportMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "bytes")


def test_migration_261_creates_combined_transport_and_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/261_combined_transport_mark.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "261_combined_transport_mark"' in source
    assert 'down_revision: str | None = "260_cabotage_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "combined_transport_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency", "bytes"):
        assert banned not in source


def test_importlinter_lists_combined_transport_on_deny() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.combined_transport_marks" in forbidden
    assert "app.models.combined_transport_mark" in forbidden


def test_api_types_include_combined_transport_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "CombinedTransportMarkResponse" in source
    assert "CombinedTransportMarkCreate" in source


def test_fga_source_declares_combined_transport_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_combined_transport_marks: member" in source


def test_fga_model_grants_combined_transport_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_combined_transport_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitCombinedTransportAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryCombinedTransportDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[CombinedTransportMark] = []

    async def list_marks(self) -> list[CombinedTransportMark]:
        return list(self.rows)

    async def persist_combined_transport_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        regime_kind: object,
        source_ref: object,
    ) -> CombinedTransportMark:
        code, kind, origin = parse_combined_transport_mark_row(
            mark_code,
            regime_kind,
            source_ref,
        )
        row = CombinedTransportMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            regime_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def combined_transport_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryCombinedTransportDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.combined_transport_marks.CombinedTransportMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitCombinedTransportAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "combined_01",
        "regime_kind": "combined",
        "source_ref": "fixture://combined-transport-mark/a",
    }
    body.update(extra)
    return body


def test_post_persists(combined_transport_http: object) -> None:
    client, desk = combined_transport_http
    response = client.post(
        "/api/v1/combined-transport-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["regime_kind"] == "combined"
    assert len(desk.rows) == 1


def test_post_rejects_amount_bytes(combined_transport_http: object) -> None:
    client, _desk = combined_transport_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/combined-transport-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_rejects_bad_code(combined_transport_http: object) -> None:
    client, _desk = combined_transport_http
    response = client.post(
        "/api/v1/combined-transport-marks",
        headers=bearer_auth_headers(),
        json=_payload(mark_code="BAD"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_post_rejects_bad_kind(combined_transport_http: object) -> None:
    client, _desk = combined_transport_http
    response = client.post(
        "/api/v1/combined-transport-marks",
        headers=bearer_auth_headers(),
        json=_payload(regime_kind="live_regime"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_rejects_foreign_source_ref(combined_transport_http: object) -> None:
    client, _desk = combined_transport_http
    response = client.post(
        "/api/v1/combined-transport-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_lists_rows(combined_transport_http: object) -> None:
    client, desk = combined_transport_http
    client.post(
        "/api/v1/combined-transport-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/combined-transport-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
