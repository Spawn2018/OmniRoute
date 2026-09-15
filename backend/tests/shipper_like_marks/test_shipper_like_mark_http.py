from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.shipper_like_mark import parse_shipper_like_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.shipper_like_mark import ShipperLikeMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount",)


def test_migration_366_creates_shipper_like_mark_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/399_shipper_like_mark.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "399_shipper_like_mark"' in source
    assert 'down_revision: str | None = "398_shipper_round_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "shipper_like_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency"):
        assert banned not in source


def test_importlinter_lists_shipper_like_mark_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.shipper_like_marks" in forbidden
    assert "app.models.shipper_like_mark" in forbidden


def test_fga_source_declares_shipper_like_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_shipper_like_marks: member" in source


def test_authorization_model_grants_shipper_like_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_shipper_like_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


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
        self.rows: list[ShipperLikeMark] = []

    async def list_marks(self) -> list[ShipperLikeMark]:
        return list(self.rows)

    async def persist_shipper_like_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        like_kind: object,
        source_ref: object,
    ) -> ShipperLikeMark:
        code, kind, origin = parse_shipper_like_mark_row(
            mark_code,
            like_kind,
            source_ref,
        )
        row = ShipperLikeMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            like_kind=kind,
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
        "app.api.shipper_like_marks.ShipperLikeMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitMarkAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "slm_match_01",
        "like_kind": "match",
        "source_ref": "fixture://shipper-like-mark/a",
    }
    body.update(extra)
    return body


def test_post_shipper_like_mark_persists(mark_http: object) -> None:
    client, desk = mark_http
    response = client.post(
        "/api/v1/shipper-like-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["like_kind"] == "match"
    assert len(desk.rows) == 1


def test_post_shipper_like_mark_rejects_amount(mark_http: object) -> None:
    client, _desk = mark_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/shipper-like-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_shipper_like_mark_rejects_bad_kind(mark_http: object) -> None:
    client, _desk = mark_http
    response = client.post(
        "/api/v1/shipper-like-marks",
        headers=bearer_auth_headers(),
        json=_payload(like_kind="award"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_shipper_like_mark_rejects_foreign_source_ref(
    mark_http: object,
) -> None:
    client, _desk = mark_http
    response = client.post(
        "/api/v1/shipper-like-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_shipper_like_marks_lists_rows(mark_http: object) -> None:
    client, desk = mark_http
    client.post(
        "/api/v1/shipper-like-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/shipper-like-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
