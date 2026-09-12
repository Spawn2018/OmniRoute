from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.dual_ledger_mark import parse_dual_ledger_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.dual_ledger_mark import DualLedgerMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]

_FORBIDDEN = ("amount", "margin", "score")


def test_migration_327_creates_dual_ledger_and_rls() -> None:
    source = (
        _ROOT / "backend/alembic/versions/327_dual_ledger_mark.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "327_dual_ledger_mark"' in source
    assert 'down_revision: str | None = "326_un_segregation_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "dual_ledger_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency"):
        assert banned not in source.lower()
    assert 'sa.Column("amount"' not in source
    assert 'sa.Column("margin"' not in source
    assert 'sa.Column("score"' not in source


def test_importlinter_lists_dual_ledger_on_deny() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.dual_ledger_marks" in forbidden
    assert "app.models.dual_ledger_mark" in forbidden


def test_api_types_include_dual_ledger_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "DualLedgerMarkResponse" in source
    assert "DualLedgerMarkCreate" in source


def test_fga_source_declares_dual_ledger_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_dual_ledger_marks: member" in source


def test_fga_model_grants_dual_ledger_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_dual_ledger_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitDualLedgerAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryDualLedgerDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[DualLedgerMark] = []

    async def list_marks(self) -> list[DualLedgerMark]:
        return list(self.rows)

    async def persist_dual_ledger_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        ledger_kind: object,
        source_ref: object,
    ) -> DualLedgerMark:
        code, kind, origin = parse_dual_ledger_mark_row(
            mark_code,
            ledger_kind,
            source_ref,
        )
        row = DualLedgerMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            ledger_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def dual_ledger_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryDualLedgerDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.dual_ledger_marks.DualLedgerMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitDualLedgerAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "dlm_ops_01",
        "ledger_kind": "ops",
        "source_ref": "fixture://dual-ledger-mark/a",
    }
    body.update(extra)
    return body


def test_post_persists(dual_ledger_http: object) -> None:
    client, desk = dual_ledger_http
    response = client.post(
        "/api/v1/dual-ledger-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["ledger_kind"] == "ops"
    assert response.headers.get("X-Omni-Catalog") == "dual-ledger-mark"
    assert len(desk.rows) == 1


def test_post_rejects_amount_margin_score(dual_ledger_http: object) -> None:
    client, _desk = dual_ledger_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/dual-ledger-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_rejects_bad_code(dual_ledger_http: object) -> None:
    client, _desk = dual_ledger_http
    response = client.post(
        "/api/v1/dual-ledger-marks",
        headers=bearer_auth_headers(),
        json=_payload(mark_code="BAD"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_post_rejects_bad_kind(dual_ledger_http: object) -> None:
    client, _desk = dual_ledger_http
    response = client.post(
        "/api/v1/dual-ledger-marks",
        headers=bearer_auth_headers(),
        json=_payload(ledger_kind="warehouse"),
    )
    assert response.status_code == 400
    assert "rodzaj ledgera" in response.json()["detail"]


def test_post_rejects_foreign_source_ref(dual_ledger_http: object) -> None:
    client, _desk = dual_ledger_http
    response = client.post(
        "/api/v1/dual-ledger-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_lists_rows(dual_ledger_http: object) -> None:
    client, desk = dual_ledger_http
    client.post(
        "/api/v1/dual-ledger-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/dual-ledger-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
