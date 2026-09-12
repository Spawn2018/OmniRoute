from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.iso_nis2_mark import parse_iso_nis2_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.iso_nis2_mark import IsoNis2Mark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "bytes")


def test_migration_275_creates_iso_nis2_and_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/275_iso_nis2_mark.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "275_iso_nis2_mark"' in source
    assert 'down_revision: str | None = "274_regulatory_radar_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "iso_nis2_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency", "bytes"):
        assert banned not in source


def test_importlinter_lists_fleet_cost_on_deny() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.iso_nis2_marks" in forbidden
    assert "app.models.iso_nis2_mark" in forbidden


def test_api_types_include_iso_nis2_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "IsoNis2MarkResponse" in source
    assert "IsoNis2MarkCreate" in source


def test_fga_source_declares_fleet_cost_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_iso_nis2_marks: member" in source


def test_fga_model_grants_fleet_cost_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_iso_nis2_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitFleetCostAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryFleetCostDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[IsoNis2Mark] = []

    async def list_marks(self) -> list[IsoNis2Mark]:
        return list(self.rows)

    async def persist_iso_nis2_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        ops_kind: object,
        source_ref: object,
    ) -> IsoNis2Mark:
        code, kind, origin = parse_iso_nis2_mark_row(
            mark_code,
            ops_kind,
            source_ref,
        )
        row = IsoNis2Mark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            ops_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def fleet_cost_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryFleetCostDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.iso_nis2_marks.IsoNis2MarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitFleetCostAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "iso_nis2_01",
        "ops_kind": "iso",
        "source_ref": "fixture://iso-nis2-mark/a",
    }
    body.update(extra)
    return body


def test_post_persists(fleet_cost_http: object) -> None:
    client, desk = fleet_cost_http
    response = client.post(
        "/api/v1/iso-nis2-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["ops_kind"] == "iso"
    assert len(desk.rows) == 1


def test_post_rejects_amount_bytes(fleet_cost_http: object) -> None:
    client, _desk = fleet_cost_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/iso-nis2-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_rejects_bad_code(fleet_cost_http: object) -> None:
    client, _desk = fleet_cost_http
    response = client.post(
        "/api/v1/iso-nis2-marks",
        headers=bearer_auth_headers(),
        json=_payload(mark_code="BAD"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_post_rejects_bad_kind(fleet_cost_http: object) -> None:
    client, _desk = fleet_cost_http
    response = client.post(
        "/api/v1/iso-nis2-marks",
        headers=bearer_auth_headers(),
        json=_payload(ops_kind="live_audit"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_rejects_foreign_source_ref(fleet_cost_http: object) -> None:
    client, _desk = fleet_cost_http
    response = client.post(
        "/api/v1/iso-nis2-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_lists_rows(fleet_cost_http: object) -> None:
    client, desk = fleet_cost_http
    client.post(
        "/api/v1/iso-nis2-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/iso-nis2-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
