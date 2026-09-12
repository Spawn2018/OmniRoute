from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.ocean_feeder_mark import parse_ocean_feeder_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.ocean_feeder_mark import OceanFeederMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]

_FORBIDDEN = ("amount", "teu", "score")


def test_migration_317_creates_ocean_feeder_and_rls() -> None:
    source = (
        _ROOT / "backend/alembic/versions/317_ocean_feeder_mark.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "317_ocean_feeder_mark"' in source
    assert 'down_revision: str | None = "316_rail_uic_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "ocean_feeder_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency"):
        assert banned not in source.lower()
    assert 'sa.Column("amount"' not in source
    assert 'sa.Column("teu"' not in source


def test_importlinter_lists_ocean_feeder_on_deny() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.ocean_feeder_marks" in forbidden
    assert "app.models.ocean_feeder_mark" in forbidden


def test_api_types_include_ocean_feeder_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "OceanFeederMarkResponse" in source
    assert "OceanFeederMarkCreate" in source


def test_fga_source_declares_ocean_feeder_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_ocean_feeder_marks: member" in source


def test_fga_model_grants_ocean_feeder_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_ocean_feeder_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitOceanFeederAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryOceanFeederDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[OceanFeederMark] = []

    async def list_marks(self) -> list[OceanFeederMark]:
        return list(self.rows)

    async def persist_ocean_feeder_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        feeder_kind: object,
        source_ref: object,
    ) -> OceanFeederMark:
        code, kind, origin = parse_ocean_feeder_mark_row(
            mark_code,
            feeder_kind,
            source_ref,
        )
        row = OceanFeederMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            feeder_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def ocean_feeder_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryOceanFeederDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.ocean_feeder_marks.OceanFeederMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitOceanFeederAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "ofm_feeder_01",
        "feeder_kind": "feeder",
        "source_ref": "fixture://ocean-feeder-mark/a",
    }
    body.update(extra)
    return body


def test_post_persists(ocean_feeder_http: object) -> None:
    client, desk = ocean_feeder_http
    response = client.post(
        "/api/v1/ocean-feeder-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["feeder_kind"] == "feeder"
    assert response.headers.get("X-Omni-Catalog") == "ocean-feeder-mark"
    assert len(desk.rows) == 1


def test_post_rejects_amount_teu_score(ocean_feeder_http: object) -> None:
    client, _desk = ocean_feeder_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/ocean-feeder-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_rejects_bad_code(ocean_feeder_http: object) -> None:
    client, _desk = ocean_feeder_http
    response = client.post(
        "/api/v1/ocean-feeder-marks",
        headers=bearer_auth_headers(),
        json=_payload(mark_code="BAD"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_post_rejects_bad_kind(ocean_feeder_http: object) -> None:
    client, _desk = ocean_feeder_http
    response = client.post(
        "/api/v1/ocean-feeder-marks",
        headers=bearer_auth_headers(),
        json=_payload(feeder_kind="alliance_live"),
    )
    assert response.status_code == 400
    assert "rodzaj feedera" in response.json()["detail"]


def test_post_rejects_foreign_source_ref(ocean_feeder_http: object) -> None:
    client, _desk = ocean_feeder_http
    response = client.post(
        "/api/v1/ocean-feeder-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_lists_rows(ocean_feeder_http: object) -> None:
    client, desk = ocean_feeder_http
    client.post(
        "/api/v1/ocean-feeder-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/ocean-feeder-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
