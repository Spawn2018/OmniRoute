from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.profit_center_mark import parse_profit_center_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.profit_center_mark import ProfitCenterMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]

_FORBIDDEN = ("amount", "margin", "score")


def test_migration_332_creates_profit_center_and_rls() -> None:
    source = (
        _ROOT / "backend/alembic/versions/332_profit_center_mark.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "332_profit_center_mark"' in source
    assert 'down_revision: str | None = "331_customer_po_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "profit_center_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency"):
        assert banned not in source.lower()
    assert 'sa.Column("amount"' not in source


def test_importlinter_lists_profit_center_on_deny() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.profit_center_marks" in forbidden
    assert "app.models.profit_center_mark" in forbidden


def test_api_types_include_profit_center_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "ProfitCenterMarkResponse" in source
    assert "ProfitCenterMarkCreate" in source


def test_fga_source_declares_profit_center_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_profit_center_marks: member" in source


def test_fga_model_grants_profit_center_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_profit_center_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitProfitCenterAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryProfitCenterDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[ProfitCenterMark] = []

    async def list_marks(self) -> list[ProfitCenterMark]:
        return list(self.rows)

    async def persist_profit_center_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        center_kind: object,
        source_ref: object,
    ) -> ProfitCenterMark:
        code, kind, origin = parse_profit_center_mark_row(
            mark_code,
            center_kind,
            source_ref,
        )
        row = ProfitCenterMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            center_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def profit_center_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryProfitCenterDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.profit_center_marks.ProfitCenterMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitProfitCenterAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "pcm_profit_01",
        "center_kind": "profit",
        "source_ref": "fixture://profit-center-mark/a",
    }
    body.update(extra)
    return body


def test_post_persists(profit_center_http: object) -> None:
    client, desk = profit_center_http
    response = client.post(
        "/api/v1/profit-center-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["center_kind"] == "profit"
    assert response.headers.get("X-Omni-Catalog") == "profit-center-mark"
    assert len(desk.rows) == 1


def test_post_rejects_amount_margin_score(profit_center_http: object) -> None:
    client, _desk = profit_center_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/profit-center-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_rejects_bad_code(profit_center_http: object) -> None:
    client, _desk = profit_center_http
    response = client.post(
        "/api/v1/profit-center-marks",
        headers=bearer_auth_headers(),
        json=_payload(mark_code="BAD"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_post_rejects_bad_kind(profit_center_http: object) -> None:
    client, _desk = profit_center_http
    response = client.post(
        "/api/v1/profit-center-marks",
        headers=bearer_auth_headers(),
        json=_payload(center_kind="allocation"),
    )
    assert response.status_code == 400
    assert "centrum" in response.json()["detail"]


def test_post_rejects_foreign_source_ref(profit_center_http: object) -> None:
    client, _desk = profit_center_http
    response = client.post(
        "/api/v1/profit-center-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_lists_rows(profit_center_http: object) -> None:
    client, desk = profit_center_http
    client.post(
        "/api/v1/profit-center-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/profit-center-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
