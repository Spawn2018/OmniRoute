from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.sales_lane import parse_sales_lane_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.sales_lane import SalesLane
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount",)


def test_migration_365_creates_sales_lane_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/365_sales_lane.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "365_sales_lane"' in source
    assert 'down_revision: str | None = "364_tracking_consent"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "sales_lane_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency"):
        assert banned not in source


def test_migration_396_adds_sales_lane_unlocode_pair() -> None:
    source = (_ROOT / "backend/alembic/versions/396_sales_lane_unlocode.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "396_sales_lane_unlocode"' in source
    assert 'down_revision: str | None = "395_crm_pipeline_mark"' in source
    assert "origin_unlocode" in source
    assert "destination_unlocode" in source
    assert "ck_sales_lane_unlocode_pair" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency"):
        assert banned not in source


def test_importlinter_lists_sales_lane_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.sales_lanes" in forbidden
    assert "app.models.sales_lane" in forbidden


def test_fga_source_declares_sales_lane_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_sales_lanes: member" in source


def test_authorization_model_grants_sales_lanes_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_sales_lanes"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitLaneAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryLaneDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[SalesLane] = []

    async def list_lanes(self) -> list[SalesLane]:
        return list(self.rows)

    async def persist_sales_lane(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        lane_code: object,
        lane_kind: object,
        source_ref: object,
        origin_unlocode: object,
        destination_unlocode: object,
    ) -> SalesLane:
        code, kind, origin, frm, to = parse_sales_lane_row(
            lane_code,
            lane_kind,
            source_ref,
            origin_unlocode,
            destination_unlocode,
        )
        row = SalesLane(
            id=uuid4(),
            organization_id=organization_id,
            lane_code=code,
            lane_kind=kind,
            origin_unlocode=frm,
            destination_unlocode=to,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def lane_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryLaneDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.sales_lanes.SalesLaneService",
        lambda _s: desk,
    )
    set_authz_checker(PermitLaneAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "lane_code": "sln_repeat_01",
        "lane_kind": "repeat",
        "origin_unlocode": "PLGDN",
        "destination_unlocode": "DEHAM",
        "source_ref": "fixture://sales-lane/a",
    }
    body.update(extra)
    return body


def test_post_sales_lane_persists(lane_http: object) -> None:
    client, desk = lane_http
    response = client.post(
        "/api/v1/sales-lanes",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["lane_kind"] == "repeat"
    assert response.json()["origin_unlocode"] == "PLGDN"
    assert len(desk.rows) == 1


def test_post_sales_lane_rejects_amount(lane_http: object) -> None:
    client, _desk = lane_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/sales-lanes",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_sales_lane_rejects_bad_kind(lane_http: object) -> None:
    client, _desk = lane_http
    response = client.post(
        "/api/v1/sales-lanes",
        headers=bearer_auth_headers(),
        json=_payload(lane_kind="pipeline"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_sales_lane_rejects_bad_unlocode(lane_http: object) -> None:
    client, _desk = lane_http
    response = client.post(
        "/api/v1/sales-lanes",
        headers=bearer_auth_headers(),
        json=_payload(origin_unlocode="XX"),
    )
    assert response.status_code == 400
    assert "para miejsc" in response.json()["detail"]


def test_post_sales_lane_rejects_foreign_source_ref(
    lane_http: object,
) -> None:
    client, _desk = lane_http
    response = client.post(
        "/api/v1/sales-lanes",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_sales_lanes_lists_rows(lane_http: object) -> None:
    client, desk = lane_http
    client.post(
        "/api/v1/sales-lanes",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/sales-lanes",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
