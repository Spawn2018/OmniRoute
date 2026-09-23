from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.local_charge_warning_mark import parse_local_charge_warning_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.local_charge_warning_mark import LocalChargeWarningMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "margin")


def test_migration_507_creates_local_charge_warning_mark_and_forces_rls() -> None:
    source = (
        _ROOT / "backend/alembic/versions/507_local_charge_warning_mark.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "507_local_charge_warning_mark"' in source
    assert 'down_revision: str | None = "506_party_contact_consent"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "local_charge_warning_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency"):
        assert banned not in source


def test_importlinter_lists_local_charge_warning_marks_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.local_charge_warning_marks" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.local_charge_warning_marks" in forbidden
    assert "app.models.local_charge_warning_mark" in forbidden


def test_fga_source_declares_local_charge_warning_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_local_charge_warning_marks: member" in source


def test_authorization_model_grants_local_charge_warning_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_local_charge_warning_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


def test_generated_api_types_include_local_charge_warning_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "LocalChargeWarningMarkResponse" in source
    assert "LocalChargeWarningMarkCreate" in source


def test_agents_forbids_local_charge_import() -> None:
    agents = (
        _ROOT / "backend/app/services/local_charge_warning_marks/AGENTS.md"
    ).read_text(encoding="utf-8")
    assert "local_charges" in agents
    assert "UPDATE / DELETE" in agents or "UPDATE / DELETE wiersza" in agents


def test_service_file_avoids_local_charge_import() -> None:
    source = (
        _ROOT
        / "backend/app/services/local_charge_warning_marks"
        / "local_charge_warning_mark_service.py"
    ).read_text(encoding="utf-8")
    assert "local_charges" not in source
    assert "charges" not in source


class PermitMarkAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryMarkDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[LocalChargeWarningMark] = []

    async def list_marks(self) -> list[LocalChargeWarningMark]:
        return list(self.rows)

    async def persist_local_charge_warning_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        warning_kind: object,
        source_ref: object,
    ) -> LocalChargeWarningMark:
        code, kind, origin = parse_local_charge_warning_mark_row(
            mark_code,
            warning_kind,
            source_ref,
        )
        row = LocalChargeWarningMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            warning_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def mark_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryMarkDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.local_charge_warning_marks.LocalChargeWarningMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitMarkAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "warn_thc_01",
        "warning_kind": "warn",
        "source_ref": "fixture://local-charge-warning/a",
    }
    body.update(extra)
    return body


def test_post_local_charge_warning_mark_persists(mark_http: object) -> None:
    client, desk = mark_http
    response = client.post(
        "/api/v1/local-charge-warning-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["warning_kind"] == "warn"
    assert len(desk.rows) == 1


def test_post_local_charge_warning_mark_rejects_bad_kind(mark_http: object) -> None:
    client, _desk = mark_http
    response = client.post(
        "/api/v1/local-charge-warning-marks",
        headers=bearer_auth_headers(),
        json=_payload(warning_kind="live"),
    )
    assert response.status_code == 400
    assert "ostrzezenie" in response.json()["detail"]


def test_post_local_charge_warning_mark_rejects_amount(mark_http: object) -> None:
    client, _desk = mark_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/local-charge-warning-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_get_local_charge_warning_marks_lists(mark_http: object) -> None:
    client, desk = mark_http
    client.post(
        "/api/v1/local-charge-warning-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/local-charge-warning-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
