from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.waste_mark import parse_waste_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.waste_mark import WasteMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "bytes")


def test_migration_443_creates_waste_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/443_waste_mark.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "443_waste_mark"' in source
    assert 'down_revision: str | None = "442_ais_import_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "waste_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency", "bytes"):
        assert banned not in source


def test_importlinter_lists_waste_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.waste_marks" in forbidden
    assert "app.models.waste_mark" in forbidden


def test_fga_source_declares_waste_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_waste_marks: member" in source


def test_authorization_model_grants_waste_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_waste_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[WasteMark] = []

    async def list_marks(self) -> list[WasteMark]:
        return list(self.rows)

    async def persist_waste_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        waste_kind: object,
        source_ref: object,
    ) -> WasteMark:
        code, kind, origin = parse_waste_mark_row(mark_code, waste_kind, source_ref)
        row = WasteMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            waste_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def waste_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.waste_marks.WasteMarkService",
        lambda _session: desk,
    )
    set_authz_checker(PermitAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "bdo_01",
        "waste_kind": "bdo",
        "source_ref": "fixture://waste-mark/a",
    }
    body.update(extra)
    return body


def test_post_waste_persists(waste_http: object) -> None:
    client, desk = waste_http
    response = client.post(
        "/api/v1/waste-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["waste_kind"] == "bdo"
    assert len(desk.rows) == 1


def test_post_waste_rejects_amount_bytes(waste_http: object) -> None:
    client, _desk = waste_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/waste-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_waste_rejects_bad_kind(waste_http: object) -> None:
    client, _desk = waste_http
    response = client.post(
        "/api/v1/waste-marks",
        headers=bearer_auth_headers(),
        json=_payload(waste_kind="amount"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_get_waste_lists_rows(waste_http: object) -> None:
    client, desk = waste_http
    client.post(
        "/api/v1/waste-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get("/api/v1/waste-marks", headers=bearer_auth_headers())
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
