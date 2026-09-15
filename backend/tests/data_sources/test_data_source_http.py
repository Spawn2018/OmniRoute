from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.data_source import parse_data_source_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.data_source import DataSource
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount",)


def test_migration_412_creates_data_source_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/412_data_source.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "412_data_source"' in source
    assert 'down_revision: str | None = "411_article50_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "data_source_tenant_isolation" in source
    assert "label_kind IN" not in source
    for banned in ("amount", "margin", "float(", "httpx", "api_key"):
        assert banned not in source


def test_importlinter_lists_data_source_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.data_sources" in forbidden
    assert "app.models.data_source" in forbidden


def test_fga_source_declares_data_source_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_data_sources: member" in source


def test_authorization_model_grants_data_sources_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_data_sources"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class DataSourceAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryDataSourceDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[DataSource] = []

    async def list_marks(self) -> list[DataSource]:
        return list(self.rows)

    async def persist_data_source(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        source_code: object,
        license_label: object,
        rights_scope: object,
        source_ref: object,
    ) -> DataSource:
        code, license_token, rights_token, origin = parse_data_source_row(
            source_code,
            license_label,
            rights_scope,
            source_ref,
        )
        row = DataSource(
            id=uuid4(),
            organization_id=organization_id,
            source_code=code,
            license_label=license_token,
            rights_scope=rights_token,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def data_source_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryDataSourceDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.data_sources.DataSourceService",
        lambda _s: desk,
    )
    set_authz_checker(DataSourceAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "source_code": "ds_openmeteo_01",
        "license_label": "CC-BY-4.0",
        "rights_scope": "weather read-only",
        "source_ref": "fixture://data-source/a",
    }
    body.update(extra)
    return body


def test_post_data_source_persists(data_source_http: object) -> None:
    client, desk = data_source_http
    response = client.post(
        "/api/v1/data-sources",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["license_label"] == "CC-BY-4.0"
    assert response.json()["rights_scope"] == "weather read-only"
    assert len(desk.rows) == 1


def test_post_data_source_rejects_amount(data_source_http: object) -> None:
    client, _desk = data_source_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/data-sources",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_data_source_rejects_short_license(data_source_http: object) -> None:
    client, _desk = data_source_http
    response = client.post(
        "/api/v1/data-sources",
        headers=bearer_auth_headers(),
        json=_payload(license_label="x"),
    )
    assert response.status_code == 400
    assert "licencja" in response.json()["detail"]


def test_post_data_source_rejects_foreign_source_ref(
    data_source_http: object,
) -> None:
    client, _desk = data_source_http
    response = client.post(
        "/api/v1/data-sources",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_data_sources_lists_rows(data_source_http: object) -> None:
    client, desk = data_source_http
    client.post(
        "/api/v1/data-sources",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/data-sources",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
