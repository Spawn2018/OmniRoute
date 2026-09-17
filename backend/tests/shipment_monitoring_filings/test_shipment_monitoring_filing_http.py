from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.shipment_monitoring_filing import parse_shipment_monitoring_filing_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.shipment_monitoring_filing import ShipmentMonitoringFiling
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "bytes")


def test_migration_433_creates_shipment_monitoring_filing_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/433_shipment_monitoring_filing.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "433_shipment_monitoring_filing"' in source
    assert 'down_revision: str | None = "432_postal_dispatch_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "shipment_monitoring_filing_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency", "bytes"):
        assert banned not in source


def test_importlinter_lists_shipment_monitoring_filing_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.shipment_monitoring_filings" in forbidden
    assert "app.models.shipment_monitoring_filing" in forbidden


def test_fga_source_declares_shipment_monitoring_filing_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_shipment_monitoring_filings: member" in source


def test_authorization_model_grants_shipment_monitoring_filings_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_shipment_monitoring_filings"]
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
        self.rows: list[ShipmentMonitoringFiling] = []

    async def list_marks(self) -> list[ShipmentMonitoringFiling]:
        return list(self.rows)

    async def persist_shipment_monitoring_filing(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        filing_code: object,
        status_kind: object,
        source_ref: object,
    ) -> ShipmentMonitoringFiling:
        code, kind, origin = parse_shipment_monitoring_filing_row(
            filing_code,
            status_kind,
            source_ref,
        )
        row = ShipmentMonitoringFiling(
            id=uuid4(),
            organization_id=organization_id,
            filing_code=code,
            status_kind=kind,
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
        "app.api.shipment_monitoring_filings.ShipmentMonitoringFilingService",
        lambda _session: desk,
    )
    set_authz_checker(PermitAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "filing_code": "filing_01",
        "status_kind": "open",
        "source_ref": "fixture://shipment-monitoring-filing/a",
    }
    body.update(extra)
    return body


def test_post_shipment_monitoring_filing_persists(invoice_alloc_http: object) -> None:
    client, desk = invoice_alloc_http
    response = client.post(
        "/api/v1/shipment-monitoring-filings",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["status_kind"] == "open"
    assert len(desk.rows) == 1


def test_post_shipment_monitoring_filing_rejects_amount_bytes(invoice_alloc_http: object) -> None:
    client, _desk = invoice_alloc_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/shipment-monitoring-filings",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_shipment_monitoring_filing_rejects_bad_kind(invoice_alloc_http: object) -> None:
    client, _desk = invoice_alloc_http
    response = client.post(
        "/api/v1/shipment-monitoring-filings",
        headers=bearer_auth_headers(),
        json=_payload(status_kind="amount"),
    )
    assert response.status_code == 400
    assert "status" in response.json()["detail"]


def test_get_shipment_monitoring_filings_lists_rows(invoice_alloc_http: object) -> None:
    client, desk = invoice_alloc_http
    client.post(
        "/api/v1/shipment-monitoring-filings",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/shipment-monitoring-filings",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
