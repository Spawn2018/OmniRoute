from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.benefit_ledger import parse_benefit_ledger_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.benefit_ledger import BenefitLedger
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "margin", "score")


def test_migration_345_creates_benefit_ledger_and_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/345_benefit_ledger.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "345_benefit_ledger"' in source
    assert 'down_revision: str | None = "344_counterfactual_run"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "benefit_ledger_tenant_isolation" in source
    for banned in ("float(", "httpx", "crps", "mae"):
        assert banned not in source.lower()
    assert 'sa.Column("amount"' not in source
    assert "charge.id" not in source


def test_importlinter_lists_benefit_ledger_on_deny() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.benefit_ledgers" in forbidden
    assert "app.models.benefit_ledger" in forbidden


def test_api_types_include_benefit_ledger() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "BenefitLedgerResponse" in source
    assert "BenefitLedgerCreate" in source


def test_fga_source_declares_benefit_ledger_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_benefit_ledgers: member" in source


def test_fga_model_grants_benefit_ledger_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_benefit_ledgers"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitBenefitLedgerAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryBenefitDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[BenefitLedger] = []

    async def list_rows(self) -> list[BenefitLedger]:
        return list(self.rows)

    async def persist_ledger(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        benefit_code: object,
        method_label: object,
        hours_saved: object,
        saved_amount: object,
        saved_currency: object,
        source_ref: object,
    ) -> BenefitLedger:
        draft = parse_benefit_ledger_row(
            benefit_code,
            method_label,
            hours_saved,
            saved_amount,
            saved_currency,
            source_ref,
        )
        row = BenefitLedger(
            id=uuid4(),
            organization_id=organization_id,
            benefit_code=draft.benefit_code,
            method_label=draft.method_label,
            hours_saved=draft.hours_saved,
            saved_amount=draft.saved_amount,
            saved_currency=draft.saved_currency,
            source_ref=draft.source_ref,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def benefit_ledger_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryBenefitDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.benefit_ledgers.BenefitLedgerService",
        lambda _s: desk,
    )
    set_authz_checker(PermitBenefitLedgerAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "benefit_code": "dock_save",
        "method_label": "porownanie z wczorajszym charge",
        "hours_saved": "2.5",
        "saved_amount": "150",
        "saved_currency": "EUR",
        "source_ref": "fixture://benefit-ledger/a",
    }
    body.update(extra)
    return body


def test_post_persists(benefit_ledger_http: object) -> None:
    client, desk = benefit_ledger_http
    response = client.post(
        "/api/v1/benefit-ledgers",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["benefit_code"] == "dock_save"
    assert response.json()["hours_saved"] == "2.5000"
    assert response.json()["saved_amount"] == "150.0000"
    assert response.headers.get("X-Omni-Catalog") == "benefit-ledger"
    assert len(desk.rows) == 1


def test_post_rejects_amount_margin_score(benefit_ledger_http: object) -> None:
    client, _desk = benefit_ledger_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/benefit-ledgers",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_rejects_float_hours(benefit_ledger_http: object) -> None:
    client, _desk = benefit_ledger_http
    response = client.post(
        "/api/v1/benefit-ledgers",
        headers=bearer_auth_headers(),
        json=_payload(hours_saved=1.5),
    )
    assert response.status_code == 422


def test_post_rejects_float_amount(benefit_ledger_http: object) -> None:
    client, _desk = benefit_ledger_http
    response = client.post(
        "/api/v1/benefit-ledgers",
        headers=bearer_auth_headers(),
        json=_payload(saved_amount=1.5),
    )
    assert response.status_code == 422


def test_post_rejects_bad_code(benefit_ledger_http: object) -> None:
    client, _desk = benefit_ledger_http
    response = client.post(
        "/api/v1/benefit-ledgers",
        headers=bearer_auth_headers(),
        json=_payload(benefit_code="1x"),
    )
    assert response.status_code == 400
    assert "kod" in response.json()["detail"]


def test_post_rejects_empty_method(benefit_ledger_http: object) -> None:
    client, _desk = benefit_ledger_http
    response = client.post(
        "/api/v1/benefit-ledgers",
        headers=bearer_auth_headers(),
        json=_payload(method_label="   "),
    )
    assert response.status_code == 400
    assert "metoda" in response.json()["detail"]


def test_post_rejects_bad_currency(benefit_ledger_http: object) -> None:
    client, _desk = benefit_ledger_http
    response = client.post(
        "/api/v1/benefit-ledgers",
        headers=bearer_auth_headers(),
        json=_payload(saved_currency="eur"),
    )
    assert response.status_code == 400
    assert "waluta" in response.json()["detail"]


def test_post_rejects_foreign_source_ref(benefit_ledger_http: object) -> None:
    client, _desk = benefit_ledger_http
    response = client.post(
        "/api/v1/benefit-ledgers",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_lists_rows(benefit_ledger_http: object) -> None:
    client, desk = benefit_ledger_http
    client.post(
        "/api/v1/benefit-ledgers",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/benefit-ledgers",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
