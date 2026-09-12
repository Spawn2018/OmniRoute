from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.diversion_mark import parse_diversion_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.diversion_mark import DiversionMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]

_FORBIDDEN = ("amount", "margin", "score")


def test_migration_337_creates_diversion_and_rls() -> None:
    source = (
        _ROOT / "backend/alembic/versions/337_diversion_mark.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "337_diversion_mark"' in source
    assert 'down_revision: str | None = "336_haulier_role_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "diversion_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency"):
        assert banned not in source.lower()
    assert 'sa.Column("amount"' not in source
    assert 'sa.Column("shipment_id"' not in source


def test_importlinter_lists_diversion_on_deny() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.diversion_marks" in forbidden
    assert "app.models.diversion_mark" in forbidden


def test_api_types_include_diversion_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "DiversionMarkResponse" in source
    assert "DiversionMarkCreate" in source


def test_fga_source_declares_diversion_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_diversion_marks: member" in source


def test_fga_model_grants_diversion_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_diversion_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitDiversionAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryDiversionDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[DiversionMark] = []

    async def list_marks(self) -> list[DiversionMark]:
        return list(self.rows)

    async def persist_diversion_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        stance_kind: object,
        source_ref: object,
    ) -> DiversionMark:
        code, kind, origin = parse_diversion_mark_row(
            mark_code,
            stance_kind,
            source_ref,
        )
        row = DiversionMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            stance_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def diversion_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryDiversionDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.diversion_marks.DiversionMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitDiversionAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "dvm_diversion_main",
        "stance_kind": "diversion",
        "source_ref": "fixture://diversion-mark/a",
    }
    body.update(extra)
    return body


def test_post_persists(diversion_http: object) -> None:
    client, desk = diversion_http
    response = client.post(
        "/api/v1/diversion-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["stance_kind"] == "diversion"
    assert response.headers.get("X-Omni-Catalog") == "diversion-mark"
    assert len(desk.rows) == 1


def test_post_rejects_amount_margin_score(diversion_http: object) -> None:
    client, _desk = diversion_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/diversion-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_rejects_bad_code(diversion_http: object) -> None:
    client, _desk = diversion_http
    response = client.post(
        "/api/v1/diversion-marks",
        headers=bearer_auth_headers(),
        json=_payload(mark_code="BAD"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_post_rejects_bad_kind(diversion_http: object) -> None:
    client, _desk = diversion_http
    response = client.post(
        "/api/v1/diversion-marks",
        headers=bearer_auth_headers(),
        json=_payload(stance_kind="carrier"),
    )
    assert response.status_code == 400
    assert "postawy" in response.json()["detail"]


def test_post_rejects_foreign_source_ref(diversion_http: object) -> None:
    client, _desk = diversion_http
    response = client.post(
        "/api/v1/diversion-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_lists_rows(diversion_http: object) -> None:
    client, desk = diversion_http
    client.post(
        "/api/v1/diversion-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/diversion-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
