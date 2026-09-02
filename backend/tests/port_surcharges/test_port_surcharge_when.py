from pathlib import Path
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import InvalidPortSurcharge, UnknownPort
from app.main import app
from app.models.port_surcharge import PortSurcharge
from app.services.port_surcharges.port_surcharge_service import PortSurchargeService
from tests.http_auth import bearer_auth_headers
from tests.port_surcharges.test_port_surcharge_http import AllowAllAuthz
from tests.port_surcharges.test_port_surcharge_service import _row, _service

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "030_port_surcharge_when.py"
_REPO = (
    _ROOT
    / "backend"
    / "app"
    / "repositories"
    / "port_surcharges"
    / "port_surcharge_repository.py"
)
_SERVICE = _ROOT / "backend" / "app" / "services" / "port_surcharges" / "port_surcharge_service.py"


def test_migration_030_indexes_when_and_downgrades() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "030_port_surcharge_when"' in source
    assert 'down_revision: str | None = "029_quotation_customer_rfq"' in source
    assert "ix_port_surcharge_org_port_when" in source
    assert "create_table" not in source
    assert "FORCE ROW LEVEL SECURITY" not in source
    assert "ix_port_surcharge_org_port_when" in source.split("def downgrade")[1]


def test_matching_sql_filters_port_and_when() -> None:
    source = _REPO.read_text(encoding="utf-8")
    assert "PortSurcharge.port_id == port_id" in source
    assert "PortSurcharge.applies_when == applies_when" in source
    assert "for " not in source.split("async def list_matching")[1].split("async def")[0]


def test_generated_api_types_include_matching() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "/api/v1/port-surcharges/matching" in source


def test_matching_service_does_not_import_charges_or_quotes() -> None:
    source = _SERVICE.read_text(encoding="utf-8")
    assert "app.services.charges" not in source
    assert "app.services.quotations" not in source
    assert "app.services.rate_lines" not in source
    assert "margin" not in source


@pytest.mark.asyncio
async def test_list_matching_normalizes_when_and_requires_port() -> None:
    service = _service()
    port_id = uuid4()
    row = _row(port_id=port_id)
    service._extras.get_port = AsyncMock(return_value=MagicMock(id=port_id))
    service._extras.list_matching = AsyncMock(return_value=[row])
    found = await service.list_matching(port_id, "  kontener 40HC w weekend  ")
    assert found == [row]
    service._extras.list_matching.assert_awaited_once_with(
        port_id,
        "kontener 40HC w weekend",
    )


@pytest.mark.asyncio
async def test_list_matching_unknown_port() -> None:
    service = _service()
    service._extras.get_port = AsyncMock(return_value=None)
    with pytest.raises(UnknownPort):
        await service.list_matching(uuid4(), "weekend")


@pytest.mark.asyncio
async def test_list_matching_rejects_blank_when() -> None:
    service = _service()
    with pytest.raises(InvalidPortSurcharge):
        await service.list_matching(uuid4(), "  ")


class _StubMatch(PortSurchargeService):
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[PortSurcharge] = []

    async def list_matching(self, port_id, applies_when):
        token = str(applies_when).strip()
        return [row for row in self.rows if row.port_id == port_id and row.applies_when == token]


@pytest.fixture
def matching_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    stub = _StubMatch(object())
    monkeypatch.setattr("app.api.port_surcharges.PortSurchargeService", lambda session: stub)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = lambda: AsyncMock()
    client = TestClient(app)
    client.extra = {"stub": stub}
    yield client
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_matching_returns_exact_when(matching_client: TestClient) -> None:
    stub = matching_client.extra["stub"]
    port_id = uuid4()
    hit = _row(port_id=port_id)
    miss = _row(port_id=port_id)
    miss.applies_when = "weekday"
    stub.rows = [hit, miss]
    response = matching_client.get(
        "/api/v1/port-surcharges/matching",
        headers=bearer_auth_headers(),
        params={"port_id": str(port_id), "applies_when": hit.applies_when},
    )
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == str(hit.id)
    assert "margin" not in body[0]
