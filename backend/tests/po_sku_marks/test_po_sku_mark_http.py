from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.po_sku_mark import parse_po_sku_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.po_sku_mark import PoSkuMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]

_FORBIDDEN = ("amount", "qty", "score")


def test_migration_324_creates_po_sku_and_rls() -> None:
    source = (
        _ROOT / "backend/alembic/versions/324_po_sku_mark.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "324_po_sku_mark"' in source
    assert 'down_revision: str | None = "323_po_plant_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "po_sku_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency"):
        assert banned not in source.lower()
    assert 'sa.Column("amount"' not in source
    assert 'sa.Column("qty"' not in source
    assert 'sa.Column("score"' not in source


def test_importlinter_lists_po_sku_on_deny() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.po_sku_marks" in forbidden
    assert "app.models.po_sku_mark" in forbidden


def test_api_types_include_po_sku_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "PoSkuMarkResponse" in source
    assert "PoSkuMarkCreate" in source


def test_fga_source_declares_po_sku_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_po_sku_marks: member" in source


def test_fga_model_grants_po_sku_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_po_sku_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitPoSkuAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryPoSkuDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[PoSkuMark] = []

    async def list_marks(self) -> list[PoSkuMark]:
        return list(self.rows)

    async def persist_po_sku_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        sku_kind: object,
        source_ref: object,
    ) -> PoSkuMark:
        code, kind, origin = parse_po_sku_mark_row(
            mark_code,
            sku_kind,
            source_ref,
        )
        row = PoSkuMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            sku_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def po_sku_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryPoSkuDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.po_sku_marks.PoSkuMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitPoSkuAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "psm_sku_01",
        "sku_kind": "sku",
        "source_ref": "fixture://po-sku-mark/a",
    }
    body.update(extra)
    return body


def test_post_persists(po_sku_http: object) -> None:
    client, desk = po_sku_http
    response = client.post(
        "/api/v1/po-sku-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["sku_kind"] == "sku"
    assert response.headers.get("X-Omni-Catalog") == "po-sku-mark"
    assert len(desk.rows) == 1


def test_post_rejects_amount_qty_score(po_sku_http: object) -> None:
    client, _desk = po_sku_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/po-sku-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_rejects_bad_code(po_sku_http: object) -> None:
    client, _desk = po_sku_http
    response = client.post(
        "/api/v1/po-sku-marks",
        headers=bearer_auth_headers(),
        json=_payload(mark_code="BAD"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_post_rejects_bad_kind(po_sku_http: object) -> None:
    client, _desk = po_sku_http
    response = client.post(
        "/api/v1/po-sku-marks",
        headers=bearer_auth_headers(),
        json=_payload(sku_kind="warehouse"),
    )
    assert response.status_code == 400
    assert "rodzaj sku" in response.json()["detail"]


def test_post_rejects_foreign_source_ref(po_sku_http: object) -> None:
    client, _desk = po_sku_http
    response = client.post(
        "/api/v1/po-sku-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_lists_rows(po_sku_http: object) -> None:
    client, desk = po_sku_http
    client.post(
        "/api/v1/po-sku-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/po-sku-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
