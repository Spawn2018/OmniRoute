from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.bonded_mark import parse_bonded_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.bonded_mark import BondedMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "wms")


def test_migration_243_creates_bonded_mark_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/243_bonded_mark.py").read_text(encoding="utf-8")
    assert 'revision: str = "243_bonded_mark"' in source
    assert 'down_revision: str | None = "242_company_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "bonded_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency", "wms"):
        assert banned not in source


def test_importlinter_lists_bonded_mark_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.bonded_marks" in forbidden
    assert "app.models.bonded_mark" in forbidden


def test_generated_api_types_include_bonded_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "BondedMarkResponse" in source
    assert "BondedMarkCreate" in source


def test_fga_source_declares_bonded_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_bonded_marks: member" in source


def test_authorization_model_grants_bonded_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_bonded_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitBondedAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryBondedDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[BondedMark] = []

    async def list_marks(self) -> list[BondedMark]:
        return list(self.rows)

    async def persist_bonded_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        bond_kind: object,
        source_ref: object,
    ) -> BondedMark:
        code, kind, origin = parse_bonded_mark_row(
            mark_code,
            bond_kind,
            source_ref,
        )
        row = BondedMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            bond_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def bonded_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryBondedDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr("app.api.bonded_marks.BondedMarkService", lambda _s: desk)
    set_authz_checker(PermitBondedAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "bond_01",
        "bond_kind": "bonded",
        "source_ref": "fixture://bonded-mark/a",
    }
    body.update(extra)
    return body


def test_post_bonded_mark_persists(bonded_http: object) -> None:
    client, desk = bonded_http
    response = client.post(
        "/api/v1/bonded-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["bond_kind"] == "bonded"
    assert len(desk.rows) == 1


def test_post_bonded_mark_rejects_amount_wms(bonded_http: object) -> None:
    client, _desk = bonded_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/bonded-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_bonded_mark_rejects_bad_kind(bonded_http: object) -> None:
    client, _desk = bonded_http
    response = client.post(
        "/api/v1/bonded-marks",
        headers=bearer_auth_headers(),
        json=_payload(bond_kind="yard"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_bonded_mark_rejects_foreign_source_ref(bonded_http: object) -> None:
    client, _desk = bonded_http
    response = client.post(
        "/api/v1/bonded-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_bonded_marks_lists_rows(bonded_http: object) -> None:
    client, desk = bonded_http
    client.post(
        "/api/v1/bonded-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/bonded-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
