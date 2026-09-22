from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.network_print_requirement import parse_network_print_requirement_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.network_print_requirement import NetworkPrintRequirement
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "bytes", "pdf", "qr")


def test_migration_498_creates_network_print_requirement_and_forces_rls() -> None:
    source = (
        _ROOT / "backend/alembic/versions/498_network_print_requirement.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "498_network_print_requirement"' in source
    assert 'down_revision: str | None = "497_groupage_tariff_volume"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "network_print_requirement_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency", "bytes"):
        assert banned not in source


def test_importlinter_lists_network_print_requirement_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.network_print_requirements" in forbidden
    assert "app.models.network_print_requirement" in forbidden


def test_generated_api_types_include_network_print_requirement() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "NetworkPrintRequirementResponse" in source
    assert "NetworkPrintRequirementCreate" in source


def test_fga_source_declares_network_print_requirement_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_network_print_requirements: member" in source


def test_authorization_model_grants_network_print_requirements_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_network_print_requirements"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitPrintAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryPrintDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[NetworkPrintRequirement] = []

    async def list_requirements(self) -> list[NetworkPrintRequirement]:
        return list(self.rows)

    async def persist_network_print_requirement(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        requirement_code: object,
        network_label: object,
        source_ref: object,
    ) -> NetworkPrintRequirement:
        code, label, origin = parse_network_print_requirement_row(
            requirement_code,
            network_label,
            source_ref,
        )
        row = NetworkPrintRequirement(
            id=uuid4(),
            organization_id=organization_id,
            requirement_code=code,
            network_label=label,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def print_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryPrintDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.network_print_requirements.NetworkPrintRequirementService",
        lambda _s: desk,
    )
    set_authz_checker(PermitPrintAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "requirement_code": "wca_label",
        "network_label": "WCA",
        "source_ref": "fixture://network-print-requirement/a",
    }
    body.update(extra)
    return body


def test_post_network_print_requirement_persists(print_http: object) -> None:
    client, desk = print_http
    response = client.post(
        "/api/v1/network-print-requirements",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["network_label"] == "WCA"
    assert len(desk.rows) == 1


def test_post_network_print_requirement_rejects_amount_bytes(print_http: object) -> None:
    client, _desk = print_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/network-print-requirements",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_network_print_requirement_rejects_bad_code(print_http: object) -> None:
    client, _desk = print_http
    response = client.post(
        "/api/v1/network-print-requirements",
        headers=bearer_auth_headers(),
        json=_payload(requirement_code="BAD"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_post_network_print_requirement_rejects_empty_label(print_http: object) -> None:
    client, _desk = print_http
    response = client.post(
        "/api/v1/network-print-requirements",
        headers=bearer_auth_headers(),
        json=_payload(network_label="   "),
    )
    assert response.status_code == 400
    assert "etykieta" in response.json()["detail"]


def test_post_network_print_requirement_rejects_foreign_source_ref(
    print_http: object,
) -> None:
    client, _desk = print_http
    response = client.post(
        "/api/v1/network-print-requirements",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_network_print_requirements_lists_rows(print_http: object) -> None:
    client, desk = print_http
    client.post(
        "/api/v1/network-print-requirements",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/network-print-requirements",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
