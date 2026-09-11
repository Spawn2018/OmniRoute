from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.legal_hold_mark import parse_legal_hold_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.legal_hold_mark import LegalHoldMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "wipe")


def test_migration_241_creates_legal_hold_mark_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/241_legal_hold_mark.py").read_text(encoding="utf-8")
    assert 'revision: str = "241_legal_hold_mark"' in source
    assert 'down_revision: str | None = "240_cmms_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "legal_hold_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency", "wipe"):
        assert banned not in source


def test_importlinter_lists_legal_hold_mark_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.legal_hold_marks" in forbidden
    assert "app.models.legal_hold_mark" in forbidden


def test_generated_api_types_include_legal_hold_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "LegalHoldMarkResponse" in source
    assert "LegalHoldMarkCreate" in source


def test_fga_source_declares_legal_hold_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_legal_hold_marks: member" in source


def test_authorization_model_grants_legal_hold_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_legal_hold_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitLegalHoldAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryLegalHoldDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[LegalHoldMark] = []

    async def list_marks(self) -> list[LegalHoldMark]:
        return list(self.rows)

    async def persist_legal_hold_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        hold_kind: object,
        source_ref: object,
    ) -> LegalHoldMark:
        code, kind, origin = parse_legal_hold_mark_row(
            mark_code,
            hold_kind,
            source_ref,
        )
        row = LegalHoldMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            hold_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def legal_hold_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryLegalHoldDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr("app.api.legal_hold_marks.LegalHoldMarkService", lambda _s: desk)
    set_authz_checker(PermitLegalHoldAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "legal_hold_wo_01",
        "hold_kind": "retention",
        "source_ref": "fixture://legal-hold-mark/a",
    }
    body.update(extra)
    return body


def test_post_legal_hold_mark_persists(legal_hold_http: object) -> None:
    client, desk = legal_hold_http
    response = client.post(
        "/api/v1/legal-hold-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["hold_kind"] == "retention"
    assert len(desk.rows) == 1


def test_post_legal_hold_mark_rejects_amount_wipe(legal_hold_http: object) -> None:
    client, _desk = legal_hold_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/legal-hold-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_legal_hold_mark_rejects_bad_kind(legal_hold_http: object) -> None:
    client, _desk = legal_hold_http
    response = client.post(
        "/api/v1/legal-hold-marks",
        headers=bearer_auth_headers(),
        json=_payload(hold_kind="crypto"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_legal_hold_mark_rejects_foreign_source_ref(legal_hold_http: object) -> None:
    client, _desk = legal_hold_http
    response = client.post(
        "/api/v1/legal-hold-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_legal_hold_marks_lists_rows(legal_hold_http: object) -> None:
    client, desk = legal_hold_http
    client.post(
        "/api/v1/legal-hold-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/legal-hold-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
