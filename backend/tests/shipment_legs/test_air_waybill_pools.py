from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.errors import InvalidShipmentLeg, ResourceNotFound
from app.domain.organization_setting import normalize_setting_key, normalize_setting_value
from app.domain.shipment_leg import require_waybill_number_prefix
from app.main import app
from app.models.shipment_leg import ShipmentLeg
from app.services.shipment_legs.shipment_leg_service import ShipmentLegService
from tests.http_auth import bearer_auth_headers
from tests.shipment_legs.test_shipment_leg_http import AllowAllAuthz

_ROOT = Path(__file__).resolve().parents[3]
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_allowlist_accepts_air_waybill_prefixes() -> None:
    assert normalize_setting_key("Hawb_Number_Prefix") == "hawb_number_prefix"
    assert normalize_setting_key("mawb_number_prefix") == "mawb_number_prefix"
    assert normalize_setting_value("hawb_number_prefix", " hawb- ") == "HAWB-"
    assert normalize_setting_value("mawb_number_prefix", "mawb.") == "MAWB."


def test_require_waybill_prefix_rejects_empty() -> None:
    with pytest.raises(InvalidShipmentLeg, match="prefiks"):
        require_waybill_number_prefix(None)
    with pytest.raises(InvalidShipmentLeg, match="prefiks"):
        require_waybill_number_prefix("  ")


def test_leg_service_does_not_read_settings_keys() -> None:
    source = (_SERVICES / "shipment_legs" / "shipment_leg_service.py").read_text(
        encoding="utf-8",
    )
    assert "organization_settings" not in source
    assert "hawb_number_prefix" not in source
    assert "mawb_number_prefix" not in source


class StubSettingsService:
    def __init__(self, session: object) -> None:
        self.hawb = "HAWB-"
        self.mawb = "MAWB-"

    async def get_setting(self, setting_key: str) -> SimpleNamespace | None:
        if setting_key == "hawb_number_prefix":
            return SimpleNamespace(setting_value=self.hawb) if self.hawb else None
        if setting_key == "mawb_number_prefix":
            return SimpleNamespace(setting_value=self.mawb) if self.mawb else None
        return None


class StubIssueLegService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[ShipmentLeg] = []

    async def issue_hawb(self, *, leg_id: UUID, prefix: str | None) -> ShipmentLeg:
        token = require_waybill_number_prefix(prefix)
        for row in self.rows:
            if row.id == leg_id:
                if row.leg_kind != "air":
                    raise InvalidShipmentLeg("list lotniczy tylko na odcinku air")
                if row.hawb_no is None:
                    row.hawb_no = f"{token}0001"
                return row
        raise ResourceNotFound("nieznany odcinek")

    async def issue_mawb(self, *, leg_id: UUID, prefix: str | None) -> ShipmentLeg:
        token = require_waybill_number_prefix(prefix)
        for row in self.rows:
            if row.id == leg_id:
                if row.leg_kind != "air":
                    raise InvalidShipmentLeg("list lotniczy tylko na odcinku air")
                if row.mawb_no is None:
                    row.mawb_no = f"{token}0001"
                return row
        raise ResourceNotFound("nieznany odcinek")


@pytest.fixture
def waybill_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    stub = StubIssueLegService(object())
    settings = StubSettingsService(object())
    air = ShipmentLeg(
        id=uuid4(),
        organization_id=uuid4(),
        shipment_id=uuid4(),
        origin_location_id=uuid4(),
        destination_location_id=uuid4(),
        leg_kind="air",
        hawb_no=None,
        mawb_no=None,
        source_ref="fixture://shipment-leg/air",
        created_by=uuid4(),
    )
    stub.rows.append(air)

    def _legs(session: object) -> StubIssueLegService:
        return stub

    def _settings(session: object) -> StubSettingsService:
        return settings

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr("app.api.shipment_legs.ShipmentLegService", _legs)
    monkeypatch.setattr("app.api.shipment_legs.OrganizationSettingService", _settings)
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), air, settings
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_issue_hawb_and_mawb(waybill_client: object) -> None:
    client, air, _settings = waybill_client
    headers = bearer_auth_headers()
    hawb = client.post(f"/api/v1/shipment-legs/{air.id}/hawb-number", headers=headers)
    assert hawb.status_code == 200
    assert hawb.json()["hawb_no"] == "HAWB-0001"
    again = client.post(f"/api/v1/shipment-legs/{air.id}/hawb-number", headers=headers)
    assert again.status_code == 200
    assert again.json()["hawb_no"] == "HAWB-0001"
    mawb = client.post(f"/api/v1/shipment-legs/{air.id}/mawb-number", headers=headers)
    assert mawb.status_code == 200
    assert mawb.json()["mawb_no"] == "MAWB-0001"


def test_http_issue_hawb_without_prefix_is_400(waybill_client: object) -> None:
    client, air, settings = waybill_client
    settings.hawb = None
    response = client.post(
        f"/api/v1/shipment-legs/{air.id}/hawb-number",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 400
    assert "prefiks" in response.json()["detail"]


@pytest.mark.asyncio
async def test_issue_returns_existing_without_rewrite() -> None:
    current = ShipmentLeg(
        id=uuid4(),
        organization_id=uuid4(),
        shipment_id=uuid4(),
        origin_location_id=uuid4(),
        destination_location_id=uuid4(),
        leg_kind="air",
        hawb_no="HAWB-0007",
        mawb_no=None,
        source_ref="fixture://shipment-leg/air",
        created_by=uuid4(),
    )
    session = AsyncMock()
    service = ShipmentLegService(session)
    service._rows.get = AsyncMock(return_value=current)
    service._rows.issue_hawb = AsyncMock()
    issued = await service.issue_hawb(leg_id=current.id, prefix="HAWB-")
    assert issued.hawb_no == "HAWB-0007"
    service._rows.issue_hawb.assert_not_awaited()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_issue_hawb_sql_increments_per_tenant(session, two_tenants) -> None:
    from app.core.database import bind_tenant
    from app.models.location import Location
    from app.repositories.shipment_legs.shipment_leg_repository import ShipmentLegRepository
    from tests.sales_invoices.test_sales_invoice_isolation import _booked

    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    async def _air_leg(*, org, user, suffix: str, hawb: str | None = None) -> ShipmentLeg:
        ship = await _booked(session, organization_id=org.id, user_id=user.id, suffix=suffix)
        origin = Location(
            id=uuid4(),
            organization_id=org.id,
            kind="postal_zone",
            name=f"{suffix} o",
            code=f"{suffix}_O",
            source_ref="tenant:manual",
            created_by=user.id,
        )
        dest = Location(
            id=uuid4(),
            organization_id=org.id,
            kind="postal_zone",
            name=f"{suffix} d",
            code=f"{suffix}_D",
            source_ref="tenant:manual",
            created_by=user.id,
        )
        session.add_all([origin, dest])
        await session.flush()
        row = ShipmentLeg(
            id=uuid4(),
            organization_id=org.id,
            shipment_id=ship.id,
            origin_location_id=origin.id,
            destination_location_id=dest.id,
            leg_kind="air",
            hawb_no=hawb,
            mawb_no=None,
            source_ref=f"fixture://shipment-leg/{suffix}",
            created_by=user.id,
        )
        session.add(row)
        await session.flush()
        return row

    await bind_tenant(session, org_a.id)
    first = await _air_leg(org=org_a, user=user_a, suffix="ia1")
    repo = ShipmentLegRepository(session)
    issued = await repo.issue_hawb(leg_id=first.id, prefix="HAWB-")
    assert issued is not None
    assert issued.hawb_no == "HAWB-0001"
    second = await _air_leg(org=org_a, user=user_a, suffix="ia2")
    again = await repo.issue_hawb(leg_id=second.id, prefix="HAWB-")
    assert again is not None
    assert again.hawb_no == "HAWB-0002"

    await bind_tenant(session, org_b.id)
    other = await _air_leg(org=org_b, user=user_b, suffix="ib1")
    foreign = await repo.issue_hawb(leg_id=other.id, prefix="HAWB-")
    assert foreign is not None
    assert foreign.hawb_no == "HAWB-0001"