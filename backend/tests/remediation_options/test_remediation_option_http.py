from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.remediation_option import parse_remediation_option_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.remediation_option import RemediationOption
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("shipment_id", "amount", "repair_cost", "expected_save")


def test_migration_227_creates_remediation_option_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/227_remediation_option.py").read_text(
        encoding="utf-8"
    )
    assert 'revision: str = "227_remediation_option"' in source
    assert 'down_revision: str | None = "226_delay_forecast"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "remediation_option_tenant_isolation" in source


def test_importlinter_lists_remediation_option_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.remediation_options" in forbidden
    assert "app.models.remediation_option" in forbidden


def test_generated_api_types_include_remediation_option() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "RemediationOptionResponse" in source
    assert "RemediationOptionCreate" in source


def test_fga_source_declares_remediation_option_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_remediation_options: member" in source


def test_authorization_model_grants_remediation_options_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_remediation_options"]
    assert relation.computed_userset is not None


class PermitRemediationAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryRemediationDesk:
    def __init__(self, session: object) -> None:
        self.options: list[RemediationOption] = []

    async def list_options(self) -> list[RemediationOption]:
        return list(self.options)

    async def persist_remediation_option(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        option_code: object,
        option_kind: object,
        source_ref: object,
    ) -> RemediationOption:
        code, kind, origin = parse_remediation_option_row(
            option_code, option_kind, source_ref
        )
        row = RemediationOption(
            id=uuid4(),
            organization_id=organization_id,
            option_code=code,
            option_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.options.append(row)
        return row


@pytest.fixture
def remediation_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryRemediationDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.remediation_options.RemediationOptionService",
        lambda _s: desk,
    )
    set_authz_checker(PermitRemediationAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "option_code": "rebook_lane_01",
        "option_kind": "rebook",
        "source_ref": "fixture://remediation-option/a",
    }
    body.update(extra)
    return body


def test_post_remediation_option_persists(remediation_http: object) -> None:
    client, desk = remediation_http
    response = client.post(
        "/api/v1/remediation-options",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["option_kind"] == "rebook"
    assert len(desk.options) == 1


def test_post_remediation_option_rejects_extra(remediation_http: object) -> None:
    client, _desk = remediation_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/remediation-options",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_remediation_option_rejects_bad_kind(remediation_http: object) -> None:
    client, _desk = remediation_http
    response = client.post(
        "/api/v1/remediation-options",
        headers=bearer_auth_headers(),
        json=_payload(option_kind="ebitda"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_remediation_option_rejects_foreign_source_ref(
    remediation_http: object,
) -> None:
    client, _desk = remediation_http
    response = client.post(
        "/api/v1/remediation-options",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_remediation_options_lists_rows(remediation_http: object) -> None:
    client, desk = remediation_http
    client.post(
        "/api/v1/remediation-options",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/remediation-options",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.options) == 1
