from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.edi_map_mark import parse_edi_map_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.edi_map_mark import EdiMapMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "payload")


def test_migration_245_creates_edi_map_mark_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/245_edi_map_mark.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "245_edi_map_mark"' in source
    assert 'down_revision: str | None = "244_filing_scheme_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "edi_map_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency", "payload"):
        assert banned not in source


def test_importlinter_lists_edi_map_mark_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.edi_map_marks" in forbidden
    assert "app.models.edi_map_mark" in forbidden


def test_generated_api_types_include_edi_map_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "EdiMapMarkResponse" in source
    assert "EdiMapMarkCreate" in source


def test_fga_source_declares_edi_map_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_edi_map_marks: member" in source


def test_authorization_model_grants_edi_map_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_edi_map_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitEdiMapAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryEdiMapDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[EdiMapMark] = []

    async def list_marks(self) -> list[EdiMapMark]:
        return list(self.rows)

    async def persist_edi_map_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        map_kind: object,
        source_ref: object,
    ) -> EdiMapMark:
        code, kind, origin = parse_edi_map_mark_row(
            mark_code,
            map_kind,
            source_ref,
        )
        row = EdiMapMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            map_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def edi_map_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryEdiMapDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.edi_map_marks.EdiMapMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitEdiMapAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "edi_map_01",
        "map_kind": "field_map",
        "source_ref": "fixture://edi-map-mark/a",
    }
    body.update(extra)
    return body


def test_post_edi_map_mark_persists(edi_map_http: object) -> None:
    client, desk = edi_map_http
    response = client.post(
        "/api/v1/edi-map-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["map_kind"] == "field_map"
    assert len(desk.rows) == 1


def test_post_edi_map_mark_rejects_amount_payload(edi_map_http: object) -> None:
    client, _desk = edi_map_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/edi-map-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_edi_map_mark_rejects_bad_code(edi_map_http: object) -> None:
    client, _desk = edi_map_http
    response = client.post(
        "/api/v1/edi-map-marks",
        headers=bearer_auth_headers(),
        json=_payload(mark_code="BAD"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_post_edi_map_mark_rejects_bad_kind(edi_map_http: object) -> None:
    client, _desk = edi_map_http
    response = client.post(
        "/api/v1/edi-map-marks",
        headers=bearer_auth_headers(),
        json=_payload(map_kind="silent_write"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_edi_map_mark_rejects_foreign_source_ref(edi_map_http: object) -> None:
    client, _desk = edi_map_http
    response = client.post(
        "/api/v1/edi-map-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_edi_map_marks_lists_rows(edi_map_http: object) -> None:
    client, desk = edi_map_http
    client.post(
        "/api/v1/edi-map-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/edi-map-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
