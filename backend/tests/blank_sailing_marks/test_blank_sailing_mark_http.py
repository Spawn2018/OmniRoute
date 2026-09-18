from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.blank_sailing_mark import parse_blank_sailing_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.blank_sailing_mark import BlankSailingMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "bytes")


def test_migration_445_creates_blank_sailing_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/445_blank_sailing_mark.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "445_blank_sailing_mark"' in source
    assert 'down_revision: str | None = "444_shipment_is_waste"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "blank_sailing_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency", "bytes"):
        assert banned not in source


def test_importlinter_lists_blank_sailing_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.blank_sailing_marks" in forbidden
    assert "app.models.blank_sailing_mark" in forbidden


def test_fga_source_declares_blank_sailing_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_blank_sailing_marks: member" in source


def test_authorization_model_grants_blank_sailing_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_blank_sailing_marks"]
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
        self.rows: list[BlankSailingMark] = []

    async def list_marks(self) -> list[BlankSailingMark]:
        return list(self.rows)

    async def persist_blank_sailing_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        sailing_kind: object,
        source_ref: object,
    ) -> BlankSailingMark:
        code, kind, origin = parse_blank_sailing_mark_row(
            mark_code,
            sailing_kind,
            source_ref,
        )
        row = BlankSailingMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            sailing_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def blank_sailing_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.blank_sailing_marks.BlankSailingMarkService",
        lambda _session: desk,
    )
    set_authz_checker(PermitAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "blank_01",
        "sailing_kind": "blank",
        "source_ref": "fixture://blank-sailing-mark/a",
    }
    body.update(extra)
    return body


def test_post_blank_sailing_persists(blank_sailing_http: object) -> None:
    client, desk = blank_sailing_http
    response = client.post(
        "/api/v1/blank-sailing-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["sailing_kind"] == "blank"
    assert len(desk.rows) == 1


def test_post_blank_sailing_rejects_amount_bytes(blank_sailing_http: object) -> None:
    client, _desk = blank_sailing_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/blank-sailing-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_blank_sailing_rejects_bad_kind(blank_sailing_http: object) -> None:
    client, _desk = blank_sailing_http
    response = client.post(
        "/api/v1/blank-sailing-marks",
        headers=bearer_auth_headers(),
        json=_payload(sailing_kind="amount"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_get_blank_sailing_lists_rows(blank_sailing_http: object) -> None:
    client, desk = blank_sailing_http
    client.post(
        "/api/v1/blank-sailing-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/blank-sailing-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
