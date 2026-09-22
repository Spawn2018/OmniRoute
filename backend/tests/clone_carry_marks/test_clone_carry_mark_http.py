from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.clone_carry_mark import parse_clone_carry_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.clone_carry_mark import CloneCarryMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "margin")


def test_migration_503_creates_clone_carry_mark_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/503_clone_carry_mark.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "503_clone_carry_mark"' in source
    assert 'down_revision: str | None = "502_pallet_synchro_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "clone_carry_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency"):
        assert banned not in source


def test_importlinter_lists_clone_carry_marks_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.clone_carry_marks" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.clone_carry_marks" in forbidden
    assert "app.models.clone_carry_mark" in forbidden


def test_fga_source_declares_clone_carry_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_clone_carry_marks: member" in source


def test_authorization_model_grants_clone_carry_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_clone_carry_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


def test_generated_api_types_include_clone_carry_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "CloneCarryMarkResponse" in source
    assert "CloneCarryMarkCreate" in source


def test_agents_forbids_clone_and_carry_import() -> None:
    agents = (
        _ROOT / "backend/app/services/clone_carry_marks/AGENTS.md"
    ).read_text(encoding="utf-8")
    assert "shipment_clone_marks" in agents
    assert "field_carry_forwards" in agents
    assert "UPDATE / DELETE" in agents or "UPDATE / DELETE wiersza" in agents


def test_service_file_avoids_clone_and_carry_import() -> None:
    source = (
        _ROOT / "backend/app/services/clone_carry_marks/clone_carry_mark_service.py"
    ).read_text(encoding="utf-8")
    assert "shipment_clone_marks" not in source
    assert "field_carry_forwards" not in source
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
        self.rows: list[CloneCarryMark] = []

    async def list_marks(self) -> list[CloneCarryMark]:
        return list(self.rows)

    async def persist_clone_carry_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        carry_kind: object,
        source_ref: object,
    ) -> CloneCarryMark:
        code, kind, origin = parse_clone_carry_mark_row(
            mark_code,
            carry_kind,
            source_ref,
        )
        row = CloneCarryMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            carry_kind=kind,
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
        "app.api.clone_carry_marks.CloneCarryMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitMarkAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "carry_on_clone_01",
        "carry_kind": "carry",
        "source_ref": "fixture://clone-carry/a",
    }
    body.update(extra)
    return body


def test_post_clone_carry_mark_persists(mark_http: object) -> None:
    client, desk = mark_http
    response = client.post(
        "/api/v1/clone-carry-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["carry_kind"] == "carry"
    assert len(desk.rows) == 1


def test_post_clone_carry_mark_rejects_bad_kind(mark_http: object) -> None:
    client, _desk = mark_http
    response = client.post(
        "/api/v1/clone-carry-marks",
        headers=bearer_auth_headers(),
        json=_payload(carry_kind="auto"),
    )
    assert response.status_code == 400
    assert "carry" in response.json()["detail"]


def test_post_clone_carry_mark_rejects_amount(mark_http: object) -> None:
    client, _desk = mark_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/clone-carry-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_get_clone_carry_marks_lists(mark_http: object) -> None:
    client, desk = mark_http
    client.post(
        "/api/v1/clone-carry-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/clone-carry-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
