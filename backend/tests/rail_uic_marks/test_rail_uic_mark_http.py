from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.rail_uic_mark import parse_rail_uic_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.rail_uic_mark import RailUicMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]

_FORBIDDEN = ("amount", "km", "score")


def test_migration_316_creates_rail_uic_and_rls() -> None:
    source = (
        _ROOT / "backend/alembic/versions/316_rail_uic_mark.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "316_rail_uic_mark"' in source
    assert 'down_revision: str | None = "315_e_doreczenia_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "rail_uic_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency"):
        assert banned not in source.lower()
    assert 'sa.Column("amount"' not in source
    assert 'sa.Column("km"' not in source


def test_importlinter_lists_rail_uic_on_deny() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.rail_uic_marks" in forbidden
    assert "app.models.rail_uic_mark" in forbidden


def test_api_types_include_rail_uic_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "RailUicMarkResponse" in source
    assert "RailUicMarkCreate" in source


def test_fga_source_declares_rail_uic_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_rail_uic_marks: member" in source


def test_fga_model_grants_rail_uic_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_rail_uic_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitRailUicAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryRailUicDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[RailUicMark] = []

    async def list_marks(self) -> list[RailUicMark]:
        return list(self.rows)

    async def persist_rail_uic_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        rail_kind: object,
        source_ref: object,
    ) -> RailUicMark:
        code, kind, origin = parse_rail_uic_mark_row(
            mark_code,
            rail_kind,
            source_ref,
        )
        row = RailUicMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            rail_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def rail_uic_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryRailUicDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.rail_uic_marks.RailUicMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitRailUicAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "rum_uic_01",
        "rail_kind": "uic",
        "source_ref": "fixture://rail-uic-mark/a",
    }
    body.update(extra)
    return body


def test_post_persists(rail_uic_http: object) -> None:
    client, desk = rail_uic_http
    response = client.post(
        "/api/v1/rail-uic-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["rail_kind"] == "uic"
    assert response.headers.get("X-Omni-Catalog") == "rail-uic-mark"
    assert len(desk.rows) == 1


def test_post_rejects_amount_km_score(rail_uic_http: object) -> None:
    client, _desk = rail_uic_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/rail-uic-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_rejects_bad_code(rail_uic_http: object) -> None:
    client, _desk = rail_uic_http
    response = client.post(
        "/api/v1/rail-uic-marks",
        headers=bearer_auth_headers(),
        json=_payload(mark_code="BAD"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_post_rejects_bad_kind(rail_uic_http: object) -> None:
    client, _desk = rail_uic_http
    response = client.post(
        "/api/v1/rail-uic-marks",
        headers=bearer_auth_headers(),
        json=_payload(rail_kind="live_rail"),
    )
    assert response.status_code == 400
    assert "rodzaj kolejowy" in response.json()["detail"]


def test_post_rejects_foreign_source_ref(rail_uic_http: object) -> None:
    client, _desk = rail_uic_http
    response = client.post(
        "/api/v1/rail-uic-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_lists_rows(rail_uic_http: object) -> None:
    client, desk = rail_uic_http
    client.post(
        "/api/v1/rail-uic-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/rail-uic-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
