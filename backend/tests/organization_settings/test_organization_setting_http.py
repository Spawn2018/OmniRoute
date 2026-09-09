from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.organization_setting import normalize_setting_key, normalize_setting_value
from app.main import app
from app.models.organization_setting import OrganizationSetting
from tests.http_auth import bearer_auth_headers


class AllowAllAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class DenyAllAuthz:
    async def check(self, *, user_id, relation, object_type, object_id) -> bool:
        return False


class StubOrganizationSettingService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[OrganizationSetting] = []

    async def list_settings(self) -> list[OrganizationSetting]:
        return list(self.rows)

    async def upsert_setting(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        setting_key: str,
        setting_value: str,
    ) -> OrganizationSetting:
        token = normalize_setting_key(setting_key)
        stored = normalize_setting_value(token, setting_value)
        row = OrganizationSetting(
            id=uuid4(),
            organization_id=organization_id,
            setting_key=token,
            setting_value=stored,
            created_by=user_id,
        )
        self.rows = [kept for kept in self.rows if kept.setting_key != token]
        self.rows.append(row)
        return row


@pytest.fixture
def settings_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    stub = StubOrganizationSettingService(object())

    def _factory(session: object) -> StubOrganizationSettingService:
        return stub

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.organization_settings.OrganizationSettingService",
        _factory,
    )
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app)
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_http_upsert_and_list_settings(settings_client: TestClient) -> None:
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = settings_client.put(
        "/api/v1/organization-settings",
        headers=headers,
        json={"setting_key": "default_currency", "setting_value": "eur"},
    )
    assert created.status_code == 200
    body = created.json()
    assert body["setting_key"] == "default_currency"
    assert body["setting_value"] == "EUR"
    assert body["organization_id"] == str(org_id)

    listed = settings_client.get("/api/v1/organization-settings", headers=headers)
    assert listed.status_code == 200
    rows = listed.json()
    assert len(rows) == 1
    assert rows[0]["id"] == body["id"]


def test_http_rejects_unknown_key(settings_client: TestClient) -> None:
    response = settings_client.put(
        "/api/v1/organization-settings",
        headers=bearer_auth_headers(),
        json={"setting_key": "loose_flag", "setting_value": "yes"},
    )
    assert response.status_code == 400
    assert "allowlist" in response.json()["detail"]


def test_http_upsert_fx_rate_basis(settings_client: TestClient) -> None:
    created = settings_client.put(
        "/api/v1/organization-settings",
        headers=bearer_auth_headers(),
        json={"setting_key": "fx_rate_basis", "setting_value": "etd"},
    )
    assert created.status_code == 200
    assert created.json()["setting_key"] == "fx_rate_basis"
    assert created.json()["setting_value"] == "etd"
    assert "margin" not in created.json()
    assert "amount" not in created.json()


def test_http_upsert_fx_rate_bad_value_is_400(settings_client: TestClient) -> None:
    basis = settings_client.put(
        "/api/v1/organization-settings",
        headers=bearer_auth_headers(),
        json={"setting_key": "fx_rate_basis", "setting_value": "margin"},
    )
    assert basis.status_code == 400
    assert "kurs" in basis.json()["detail"]
    offset = settings_client.put(
        "/api/v1/organization-settings",
        headers=bearer_auth_headers(),
        json={"setting_key": "fx_rate_offset_days", "setting_value": "2"},
    )
    assert offset.status_code == 400
    assert "dni" in offset.json()["detail"]


def test_list_settings_forbidden_without_permission() -> None:
    set_authz_checker(DenyAllAuthz())
    client = TestClient(app)
    response = client.get(
        "/api/v1/organization-settings",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 403
    set_authz_checker(None)
