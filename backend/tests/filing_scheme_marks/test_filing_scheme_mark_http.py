from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.filing_scheme_mark import parse_filing_scheme_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.filing_scheme_mark import FilingSchemeMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "sent")


def test_migration_244_creates_filing_scheme_mark_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/244_filing_scheme_mark.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "244_filing_scheme_mark"' in source
    assert 'down_revision: str | None = "243_bonded_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "filing_scheme_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency", "sent"):
        assert banned not in source


def test_importlinter_lists_filing_scheme_mark_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.filing_scheme_marks" in forbidden
    assert "app.models.filing_scheme_mark" in forbidden


def test_generated_api_types_include_filing_scheme_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "FilingSchemeMarkResponse" in source
    assert "FilingSchemeMarkCreate" in source


def test_fga_source_declares_filing_scheme_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_filing_scheme_marks: member" in source


def test_authorization_model_grants_filing_scheme_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_filing_scheme_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitFilingSchemeAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryFilingSchemeDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[FilingSchemeMark] = []

    async def list_marks(self) -> list[FilingSchemeMark]:
        return list(self.rows)

    async def persist_filing_scheme_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        scheme_kind: object,
        source_ref: object,
    ) -> FilingSchemeMark:
        code, kind, origin = parse_filing_scheme_mark_row(
            mark_code,
            scheme_kind,
            source_ref,
        )
        row = FilingSchemeMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            scheme_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def filing_scheme_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryFilingSchemeDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.filing_scheme_marks.FilingSchemeMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitFilingSchemeAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "filing_ics2_01",
        "scheme_kind": "ics2",
        "source_ref": "fixture://filing-scheme-mark/a",
    }
    body.update(extra)
    return body


def test_post_filing_scheme_mark_persists(filing_scheme_http: object) -> None:
    client, desk = filing_scheme_http
    response = client.post(
        "/api/v1/filing-scheme-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["scheme_kind"] == "ics2"
    assert len(desk.rows) == 1


def test_post_filing_scheme_mark_rejects_amount_sent(filing_scheme_http: object) -> None:
    client, _desk = filing_scheme_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/filing-scheme-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_filing_scheme_mark_rejects_bad_code(filing_scheme_http: object) -> None:
    client, _desk = filing_scheme_http
    response = client.post(
        "/api/v1/filing-scheme-marks",
        headers=bearer_auth_headers(),
        json=_payload(mark_code="BAD"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_post_filing_scheme_mark_rejects_bad_kind(filing_scheme_http: object) -> None:
    client, _desk = filing_scheme_http
    response = client.post(
        "/api/v1/filing-scheme-marks",
        headers=bearer_auth_headers(),
        json=_payload(scheme_kind="sent-ue"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_filing_scheme_mark_rejects_foreign_source_ref(filing_scheme_http: object) -> None:
    client, _desk = filing_scheme_http
    response = client.post(
        "/api/v1/filing-scheme-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_filing_scheme_marks_lists_rows(filing_scheme_http: object) -> None:
    client, desk = filing_scheme_http
    client.post(
        "/api/v1/filing-scheme-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/filing-scheme-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
