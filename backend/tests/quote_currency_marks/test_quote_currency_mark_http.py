from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.quote_currency_mark import parse_quote_currency_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.quote_currency_mark import QuoteCurrencyMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]

_FORBIDDEN = ("amount", "margin", "score")

def test_migration_340_creates_quote_currency_and_rls() -> None:
    source = (
        _ROOT / "backend/alembic/versions/340_quote_currency_mark.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "340_quote_currency_mark"' in source
    assert 'down_revision: str | None = "339_bid_decision_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "quote_currency_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx"):
        assert banned not in source.lower()
    assert 'sa.Column("amount"' not in source
    assert 'sa.Column("quotation_id"' not in source


def test_importlinter_lists_quote_currency_on_deny() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.quote_currency_marks" in forbidden
    assert "app.models.quote_currency_mark" in forbidden

def test_api_types_include_quote_currency_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "QuoteCurrencyMarkResponse" in source
    assert "QuoteCurrencyMarkCreate" in source

def test_fga_source_declares_bid_decision_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_quote_currency_marks: member" in source

def test_fga_model_grants_bid_decision_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_quote_currency_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"

class PermitQuoteCurrencyAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True

class InMemoryQuoteCurrencyDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[QuoteCurrencyMark] = []

    async def list_marks(self) -> list[QuoteCurrencyMark]:
        return list(self.rows)

    async def persist_quote_currency_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        currency_kind: object,
        source_ref: object,
    ) -> QuoteCurrencyMark:
        code, kind, origin = parse_quote_currency_mark_row(
            mark_code,
            currency_kind,
            source_ref,
        )
        row = QuoteCurrencyMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            currency_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row

@pytest.fixture
def bid_decision_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryQuoteCurrencyDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.quote_currency_marks.QuoteCurrencyMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitQuoteCurrencyAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)

def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "qcm_account_main",
        "currency_kind": "account",
        "source_ref": "fixture://quote-currency-mark/a",
    }
    body.update(extra)
    return body

def test_post_persists(bid_decision_http: object) -> None:
    client, desk = bid_decision_http
    response = client.post(
        "/api/v1/quote-currency-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["currency_kind"] == "account"
    assert response.headers.get("X-Omni-Catalog") == "quote-currency-mark"
    assert len(desk.rows) == 1

def test_post_rejects_amount_margin_score(bid_decision_http: object) -> None:
    client, _desk = bid_decision_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/quote-currency-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field

def test_post_rejects_bad_code(bid_decision_http: object) -> None:
    client, _desk = bid_decision_http
    response = client.post(
        "/api/v1/quote-currency-marks",
        headers=bearer_auth_headers(),
        json=_payload(mark_code="BAD"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]

def test_post_rejects_bad_kind(bid_decision_http: object) -> None:
    client, _desk = bid_decision_http
    response = client.post(
        "/api/v1/quote-currency-marks",
        headers=bearer_auth_headers(),
        json=_payload(currency_kind="fx"),
    )
    assert response.status_code == 400
    assert "waluty" in response.json()["detail"]

def test_post_rejects_foreign_source_ref(bid_decision_http: object) -> None:
    client, _desk = bid_decision_http
    response = client.post(
        "/api/v1/quote-currency-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]

def test_get_lists_rows(bid_decision_http: object) -> None:
    client, desk = bid_decision_http
    client.post(
        "/api/v1/quote-currency-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/quote-currency-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
