from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.sanctions_mark import parse_sanctions_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.sanctions_mark import SanctionsMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "bytes")


def test_migration_254_creates_sanctions_mark_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/254_sanctions_mark.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "254_sanctions_mark"' in source
    assert 'down_revision: str | None = "253_cargo_cover_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "sanctions_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency", "bytes"):
        assert banned not in source


def test_importlinter_lists_sanctions_mark_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.sanctions_marks" in forbidden
    assert "app.models.sanctions_mark" in forbidden


def test_generated_api_types_include_sanctions_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "SanctionsMarkResponse" in source
    assert "SanctionsMarkCreate" in source


def test_fga_source_declares_sanctions_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_sanctions_marks: member" in source


def test_authorization_model_grants_sanctions_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_sanctions_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitSanctionsAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemorySanctionsDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[SanctionsMark] = []

    async def list_marks(self) -> list[SanctionsMark]:
        return list(self.rows)

    async def persist_sanctions_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        list_kind: object,
        source_ref: object,
    ) -> SanctionsMark:
        code, kind, origin = parse_sanctions_mark_row(
            mark_code,
            list_kind,
            source_ref,
        )
        row = SanctionsMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            list_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def sanctions_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemorySanctionsDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.sanctions_marks.SanctionsMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitSanctionsAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "ofac_01",
        "list_kind": "ofac",
        "source_ref": "fixture://sanctions-mark/a",
    }
    body.update(extra)
    return body


def test_post_sanctions_mark_persists(sanctions_http: object) -> None:
    client, desk = sanctions_http
    response = client.post(
        "/api/v1/sanctions-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["list_kind"] == "ofac"
    assert len(desk.rows) == 1


def test_post_sanctions_mark_rejects_amount_bytes(sanctions_http: object) -> None:
    client, _desk = sanctions_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/sanctions-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_sanctions_mark_rejects_bad_code(sanctions_http: object) -> None:
    client, _desk = sanctions_http
    response = client.post(
        "/api/v1/sanctions-marks",
        headers=bearer_auth_headers(),
        json=_payload(mark_code="BAD"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_post_sanctions_mark_rejects_bad_kind(sanctions_http: object) -> None:
    client, _desk = sanctions_http
    response = client.post(
        "/api/v1/sanctions-marks",
        headers=bearer_auth_headers(),
        json=_payload(list_kind="engine"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_sanctions_mark_rejects_foreign_source_ref(sanctions_http: object) -> None:
    client, _desk = sanctions_http
    response = client.post(
        "/api/v1/sanctions-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_sanctions_marks_lists_rows(sanctions_http: object) -> None:
    client, desk = sanctions_http
    client.post(
        "/api/v1/sanctions-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/sanctions-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
