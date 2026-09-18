from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.create_block_mark import parse_create_block_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.create_block_mark import CreateBlockMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "bytes")


def test_migration_436_creates_create_block_mark_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/436_create_block_mark.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "436_create_block_mark"' in source
    assert 'down_revision: str | None = "435_invoice_match_cand"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "create_block_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency", "bytes"):
        assert banned not in source


def test_importlinter_lists_create_block_mark_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.create_block_marks" in forbidden
    assert "app.models.create_block_mark" in forbidden


def test_fga_source_declares_create_block_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_create_block_marks: member" in source


def test_authorization_model_grants_create_block_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_create_block_marks"]
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
        self.rows: list[CreateBlockMark] = []

    async def list_marks(self) -> list[CreateBlockMark]:
        return list(self.rows)

    async def persist_create_block_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        block_kind: object,
        source_ref: object,
    ) -> CreateBlockMark:
        code, kind, origin = parse_create_block_mark_row(
            mark_code,
            block_kind,
            source_ref,
        )
        row = CreateBlockMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            block_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def create_block_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.create_block_marks.CreateBlockMarkService",
        lambda _session: desk,
    )
    set_authz_checker(PermitAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "gate_01",
        "block_kind": "block",
        "source_ref": "fixture://create-block-mark/a",
    }
    body.update(extra)
    return body


def test_post_create_block_mark_persists(create_block_http: object) -> None:
    client, desk = create_block_http
    response = client.post(
        "/api/v1/create-block-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["block_kind"] == "block"
    assert len(desk.rows) == 1


def test_post_create_block_rejects_amount_bytes(create_block_http: object) -> None:
    client, _desk = create_block_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/create-block-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_create_block_mark_rejects_bad_kind(create_block_http: object) -> None:
    client, _desk = create_block_http
    response = client.post(
        "/api/v1/create-block-marks",
        headers=bearer_auth_headers(),
        json=_payload(block_kind="amount"),
    )
    assert response.status_code == 400
    assert "brama" in response.json()["detail"]


def test_get_create_block_marks_lists_rows(create_block_http: object) -> None:
    client, desk = create_block_http
    client.post(
        "/api/v1/create-block-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/create-block-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
