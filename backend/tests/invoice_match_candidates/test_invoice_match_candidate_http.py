from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.invoice_match_candidate import parse_invoice_match_candidate_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.invoice_match_candidate import InvoiceMatchCandidate
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "bytes")


def test_migration_435_creates_invoice_match_candidate_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/435_invoice_match_cand.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "435_invoice_match_cand"' in source
    assert 'down_revision: str | None = "434_rel_doc_requirement"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "invoice_match_candidate_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency", "bytes"):
        assert banned not in source


def test_importlinter_lists_invoice_match_candidate_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.invoice_match_candidates" in forbidden
    assert "app.models.invoice_match_candidate" in forbidden


def test_fga_source_declares_invoice_match_candidate_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_invoice_match_candidates: member" in source


def test_authorization_model_grants_invoice_match_candidates_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_invoice_match_candidates"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[InvoiceMatchCandidate] = []

    async def list_marks(self) -> list[InvoiceMatchCandidate]:
        return list(self.rows)

    async def persist_invoice_match_candidate(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        candidate_code: object,
        candidate_kind: object,
        source_ref: object,
    ) -> InvoiceMatchCandidate:
        code, kind, origin = parse_invoice_match_candidate_row(
            candidate_code,
            candidate_kind,
            source_ref,
        )
        row = InvoiceMatchCandidate(
            id=uuid4(),
            organization_id=organization_id,
            candidate_code=code,
            candidate_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def invoice_alloc_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.invoice_match_candidates.InvoiceMatchCandidateService",
        lambda _session: desk,
    )
    set_authz_checker(PermitAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "candidate_code": "cand_01",
        "candidate_kind": "proposed",
        "source_ref": "fixture://invoice-match-candidate/a",
    }
    body.update(extra)
    return body


def test_post_invoice_match_candidate_persists(invoice_alloc_http: object) -> None:
    client, desk = invoice_alloc_http
    response = client.post(
        "/api/v1/invoice-match-candidates",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["candidate_kind"] == "proposed"
    assert len(desk.rows) == 1


def test_post_rel_doc_req_rejects_amount_bytes(invoice_alloc_http: object) -> None:
    client, _desk = invoice_alloc_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/invoice-match-candidates",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_invoice_match_candidate_rejects_bad_kind(invoice_alloc_http: object) -> None:
    client, _desk = invoice_alloc_http
    response = client.post(
        "/api/v1/invoice-match-candidates",
        headers=bearer_auth_headers(),
        json=_payload(candidate_kind="amount"),
    )
    assert response.status_code == 400
    assert "kandydat" in response.json()["detail"]


def test_get_invoice_match_candidates_lists_rows(invoice_alloc_http: object) -> None:
    client, desk = invoice_alloc_http
    client.post(
        "/api/v1/invoice-match-candidates",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/invoice-match-candidates",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
