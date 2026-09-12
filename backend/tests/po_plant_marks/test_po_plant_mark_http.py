from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.po_plant_mark import parse_po_plant_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.po_plant_mark import PoPlantMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]

_FORBIDDEN = ("amount", "qty", "score")


def test_migration_323_creates_po_plant_and_rls() -> None:
    source = (
        _ROOT / "backend/alembic/versions/323_po_plant_mark.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "323_po_plant_mark"' in source
    assert 'down_revision: str | None = "322_demo_sim_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "po_plant_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency"):
        assert banned not in source.lower()
    assert 'sa.Column("amount"' not in source
    assert 'sa.Column("qty"' not in source
    assert 'sa.Column("score"' not in source


def test_importlinter_lists_po_plant_on_deny() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.po_plant_marks" in forbidden
    assert "app.models.po_plant_mark" in forbidden


def test_api_types_include_po_plant_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "PoPlantMarkResponse" in source
    assert "PoPlantMarkCreate" in source


def test_fga_source_declares_po_plant_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_po_plant_marks: member" in source


def test_fga_model_grants_po_plant_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_po_plant_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitPoPlantAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryPoPlantDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[PoPlantMark] = []

    async def list_marks(self) -> list[PoPlantMark]:
        return list(self.rows)

    async def persist_po_plant_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        plant_kind: object,
        source_ref: object,
    ) -> PoPlantMark:
        code, kind, origin = parse_po_plant_mark_row(
            mark_code,
            plant_kind,
            source_ref,
        )
        row = PoPlantMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            plant_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def po_plant_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryPoPlantDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.po_plant_marks.PoPlantMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitPoPlantAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "ppm_plant_01",
        "plant_kind": "plant",
        "source_ref": "fixture://po-plant-mark/a",
    }
    body.update(extra)
    return body


def test_post_persists(po_plant_http: object) -> None:
    client, desk = po_plant_http
    response = client.post(
        "/api/v1/po-plant-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["plant_kind"] == "plant"
    assert response.headers.get("X-Omni-Catalog") == "po-plant-mark"
    assert len(desk.rows) == 1


def test_post_rejects_amount_qty_score(po_plant_http: object) -> None:
    client, _desk = po_plant_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/po-plant-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_rejects_bad_code(po_plant_http: object) -> None:
    client, _desk = po_plant_http
    response = client.post(
        "/api/v1/po-plant-marks",
        headers=bearer_auth_headers(),
        json=_payload(mark_code="BAD"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_post_rejects_bad_kind(po_plant_http: object) -> None:
    client, _desk = po_plant_http
    response = client.post(
        "/api/v1/po-plant-marks",
        headers=bearer_auth_headers(),
        json=_payload(plant_kind="warehouse"),
    )
    assert response.status_code == 400
    assert "rodzaj plant" in response.json()["detail"]


def test_post_rejects_foreign_source_ref(po_plant_http: object) -> None:
    client, _desk = po_plant_http
    response = client.post(
        "/api/v1/po-plant-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_lists_rows(po_plant_http: object) -> None:
    client, desk = po_plant_http
    client.post(
        "/api/v1/po-plant-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/po-plant-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
