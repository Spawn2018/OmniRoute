from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import InvalidOceanBill, ResourceNotFound
from app.domain.ocean_bill import require_bill_number_prefix
from app.domain.organization_setting import normalize_setting_key, normalize_setting_value
from app.main import app
from app.models.ocean_bill import OceanBill
from app.services.ocean_bills.ocean_bill_service import OceanBillService
from tests.http_auth import bearer_auth_headers
from tests.ocean_bills.test_ocean_bill_http import AllowAllAuthz

_ROOT = Path(__file__).resolve().parents[3]
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_allowlist_accepts_ocean_bill_prefixes() -> None:
    assert normalize_setting_key("Hbl_Number_Prefix") == "hbl_number_prefix"
    assert normalize_setting_key("mbl_number_prefix") == "mbl_number_prefix"
    assert normalize_setting_value("hbl_number_prefix", " hbl- ") == "HBL-"
    assert normalize_setting_value("mbl_number_prefix", "mbl.") == "MBL."


def test_require_bill_prefix_rejects_empty() -> None:
    with pytest.raises(InvalidOceanBill, match="prefiks"):
        require_bill_number_prefix(None)
    with pytest.raises(InvalidOceanBill, match="prefiks"):
        require_bill_number_prefix("  ")


def test_bill_service_does_not_read_settings_keys() -> None:
    source = (_SERVICES / "ocean_bills" / "ocean_bill_service.py").read_text(
        encoding="utf-8",
    )
    assert "organization_settings" not in source
    assert "hbl_number_prefix" not in source
    assert "mbl_number_prefix" not in source


class StubSettingsService:
    def __init__(self, session: object) -> None:
        self.hbl = "HBL-"
        self.mbl = "MBL-"

    async def get_setting(self, setting_key: str) -> SimpleNamespace | None:
        if setting_key == "hbl_number_prefix":
            return SimpleNamespace(setting_value=self.hbl) if self.hbl else None
        if setting_key == "mbl_number_prefix":
            return SimpleNamespace(setting_value=self.mbl) if self.mbl else None
        return None


class StubIssueBillService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[OceanBill] = []

    async def issue_hbl(self, *, bill_id: UUID, prefix: str | None) -> OceanBill:
        token = require_bill_number_prefix(prefix)
        for row in self.rows:
            if row.id == bill_id:
                if row.bill_kind != "hbl":
                    raise InvalidOceanBill("nadanie HBL tylko dla bill_kind hbl")
                if row.bill_no is None:
                    row.bill_no = f"{token}0001"
                return row
        raise ResourceNotFound("nieznany konosament")

    async def issue_mbl(self, *, bill_id: UUID, prefix: str | None) -> OceanBill:
        token = require_bill_number_prefix(prefix)
        for row in self.rows:
            if row.id == bill_id:
                if row.bill_kind != "mbl":
                    raise InvalidOceanBill("nadanie MBL tylko dla bill_kind mbl")
                if row.bill_no is None:
                    row.bill_no = f"{token}0001"
                return row
        raise ResourceNotFound("nieznany konosament")


@pytest.fixture
def bill_pool_client(monkeypatch: pytest.MonkeyPatch) -> object:
    stub = StubIssueBillService(object())
    settings = StubSettingsService(object())
    hbl = OceanBill(
        id=uuid4(),
        organization_id=uuid4(),
        shipment_id=uuid4(),
        bill_no=None,
        bill_kind="hbl",
        source_ref="fixture://ocean-bill/hbl",
        created_by=uuid4(),
    )
    mbl = OceanBill(
        id=uuid4(),
        organization_id=uuid4(),
        shipment_id=uuid4(),
        bill_no=None,
        bill_kind="mbl",
        source_ref="fixture://ocean-bill/mbl",
        created_by=uuid4(),
    )
    stub.rows.extend([hbl, mbl])

    def _bills(session: object) -> StubIssueBillService:
        return stub

    def _settings(session: object) -> StubSettingsService:
        return settings

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.ocean_bills.OceanBillService", _bills)
    monkeypatch.setattr("app.api.ocean_bills.OrganizationSettingService", _settings)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), hbl, mbl, settings
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_issue_hbl_and_mbl(bill_pool_client: object) -> None:
    client, hbl, mbl, _settings = bill_pool_client
    headers = bearer_auth_headers()
    issued = client.post(f"/api/v1/ocean-bills/{hbl.id}/hbl-number", headers=headers)
    assert issued.status_code == 200
    assert issued.json()["bill_no"] == "HBL-0001"
    again = client.post(f"/api/v1/ocean-bills/{hbl.id}/hbl-number", headers=headers)
    assert again.status_code == 200
    assert again.json()["bill_no"] == "HBL-0001"
    master = client.post(f"/api/v1/ocean-bills/{mbl.id}/mbl-number", headers=headers)
    assert master.status_code == 200
    assert master.json()["bill_no"] == "MBL-0001"


def test_http_issue_hbl_without_prefix_is_400(bill_pool_client: object) -> None:
    client, hbl, _mbl, settings = bill_pool_client
    settings.hbl = None
    response = client.post(
        f"/api/v1/ocean-bills/{hbl.id}/hbl-number",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 400
    assert "prefiks" in response.json()["detail"]


def test_http_issue_hbl_on_mbl_is_400(bill_pool_client: object) -> None:
    client, _hbl, mbl, _settings = bill_pool_client
    response = client.post(
        f"/api/v1/ocean-bills/{mbl.id}/hbl-number",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 400
    assert "hbl" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_issue_returns_existing_without_rewrite() -> None:
    current = OceanBill(
        id=uuid4(),
        organization_id=uuid4(),
        shipment_id=uuid4(),
        bill_no="HBL-0007",
        bill_kind="hbl",
        source_ref="fixture://ocean-bill/hbl",
        created_by=uuid4(),
    )
    session = AsyncMock()
    service = OceanBillService(session)
    service._rows.get = AsyncMock(return_value=current)
    service._rows.issue_hbl = AsyncMock()
    issued = await service.issue_hbl(bill_id=current.id, prefix="HBL-")
    assert issued.bill_no == "HBL-0007"
    service._rows.issue_hbl.assert_not_awaited()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_issue_hbl_sql_increments_per_tenant(session, two_tenants) -> None:
    from app.core.database import bind_tenant
    from app.repositories.ocean_bills.ocean_bill_repository import OceanBillRepository
    from tests.sales_invoices.test_sales_invoice_isolation import _booked

    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    async def _hbl(*, org, user, suffix: str, bill_no: str | None = None) -> OceanBill:
        ship = await _booked(session, organization_id=org.id, user_id=user.id, suffix=suffix)
        row = OceanBill(
            id=uuid4(),
            organization_id=org.id,
            shipment_id=ship.id,
            bill_no=bill_no,
            bill_kind="hbl",
            source_ref=f"fixture://ocean-bill/{suffix}",
            created_by=user.id,
        )
        session.add(row)
        await session.flush()
        return row

    await bind_tenant(session, org_a.id)
    first = await _hbl(org=org_a, user=user_a, suffix="ob1")
    repo = OceanBillRepository(session)
    issued = await repo.issue_hbl(bill_id=first.id, prefix="HBL-")
    assert issued is not None
    assert issued.bill_no == "HBL-0001"
    second = await _hbl(org=org_a, user=user_a, suffix="ob2")
    again = await repo.issue_hbl(bill_id=second.id, prefix="HBL-")
    assert again is not None
    assert again.bill_no == "HBL-0002"

    await bind_tenant(session, org_b.id)
    other = await _hbl(org=org_b, user=user_b, suffix="obb1")
    foreign = await repo.issue_hbl(bill_id=other.id, prefix="HBL-")
    assert foreign is not None
    assert foreign.bill_no == "HBL-0001"
