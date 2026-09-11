from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.spend_mark import parse_spend_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.spend_mark import SpendMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "margin")


def test_migration_232_creates_spend_mark_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/232_spend_mark.py").read_text(
        encoding="utf-8"
    )
    assert 'revision: str = "232_spend_mark"' in source
    assert 'down_revision: str | None = "231_repair_playbook"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "spend_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency"):
        assert banned not in source


def test_importlinter_lists_spend_mark_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.spend_marks" in forbidden
    assert "app.models.spend_mark" in forbidden


def test_generated_api_types_include_spend_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "SpendMarkResponse" in source
    assert "SpendMarkCreate" in source


def test_fga_source_declares_spend_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_spend_marks: member" in source


def test_authorization_model_grants_spend_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_spend_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitSpendAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemorySpendDesk:
    def __init__(self, session: object) -> None:
        self.marks: list[SpendMark] = []

    async def list_marks(self) -> list[SpendMark]:
        return list(self.marks)

    async def persist_spend_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        leakage_kind: object,
        source_ref: object,
    ) -> SpendMark:
        code, kind, origin = parse_spend_mark_row(mark_code, leakage_kind, source_ref)
        row = SpendMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            leakage_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.marks.append(row)
        return row


@pytest.fixture
def spend_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemorySpendDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.spend_marks.SpendMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitSpendAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "invoice_leak_01",
        "leakage_kind": "invoice",
        "source_ref": "fixture://spend-mark/a",
    }
    body.update(extra)
    return body


def test_post_spend_mark_persists(spend_http: object) -> None:
    client, desk = spend_http
    response = client.post(
        "/api/v1/spend-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["leakage_kind"] == "invoice"
    assert len(desk.marks) == 1


def test_post_spend_mark_rejects_amount_margin(spend_http: object) -> None:
    client, _desk = spend_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/spend-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_spend_mark_rejects_bad_kind(spend_http: object) -> None:
    client, _desk = spend_http
    response = client.post(
        "/api/v1/spend-marks",
        headers=bearer_auth_headers(),
        json=_payload(leakage_kind="sql_fv"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_spend_mark_rejects_foreign_source_ref(spend_http: object) -> None:
    client, _desk = spend_http
    response = client.post(
        "/api/v1/spend-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_spend_marks_lists_rows(spend_http: object) -> None:
    client, desk = spend_http
    client.post(
        "/api/v1/spend-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/spend-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.marks) == 1
