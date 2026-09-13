from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.nac_mark import parse_nac_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.nac_mark import NacMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount",)


def test_migration_374_creates_nac_mark_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/374_nac_mark.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "374_nac_mark"' in source
    assert 'down_revision: str | None = "373_lcl_console_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "nac_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency", "shipment_stakeholder"):
        assert banned not in source


def test_importlinter_lists_nac_mark_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.nac_marks" in forbidden
    assert "app.models.nac_mark" in forbidden


def test_fga_source_declares_nac_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_nac_marks: member" in source


def test_authorization_model_grants_nac_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_nac_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class NacMarkAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryNacDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[NacMark] = []

    async def list_marks(self) -> list[NacMark]:
        return list(self.rows)

    async def persist_nac_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        nac_kind: object,
        source_ref: object,
    ) -> NacMark:
        code, kind, origin = parse_nac_mark_row(
            mark_code,
            nac_kind,
            source_ref,
        )
        row = NacMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            nac_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def nac_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryNacDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.nac_marks.NacMarkService",
        lambda _s: desk,
    )
    set_authz_checker(NacMarkAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "nac_agent_01",
        "nac_kind": "agent",
        "source_ref": "fixture://nac-mark/a",
    }
    body.update(extra)
    return body


def test_post_nac_mark_persists(nac_http: object) -> None:
    client, desk = nac_http
    response = client.post(
        "/api/v1/nac-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["nac_kind"] == "agent"
    assert len(desk.rows) == 1


def test_post_nac_mark_rejects_amount(nac_http: object) -> None:
    client, _desk = nac_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/nac-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_nac_mark_rejects_bad_kind(nac_http: object) -> None:
    client, _desk = nac_http
    response = client.post(
        "/api/v1/nac-marks",
        headers=bearer_auth_headers(),
        json=_payload(nac_kind="live_http"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_nac_mark_rejects_foreign_source_ref(nac_http: object) -> None:
    client, _desk = nac_http
    response = client.post(
        "/api/v1/nac-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_nac_marks_lists_rows(nac_http: object) -> None:
    client, desk = nac_http
    client.post(
        "/api/v1/nac-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/nac-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
