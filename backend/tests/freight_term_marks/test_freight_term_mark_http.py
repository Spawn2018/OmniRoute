from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.freight_term_mark import parse_freight_term_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.freight_term_mark import FreightTermMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]

_FORBIDDEN = ("amount", "margin", "score")


def test_migration_330_creates_freight_term_and_rls() -> None:
    source = (
        _ROOT / "backend/alembic/versions/330_freight_term_mark.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "330_freight_term_mark"' in source
    assert 'down_revision: str | None = "329_slot_guarantee_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "freight_term_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency"):
        assert banned not in source.lower()
    assert 'sa.Column("amount"' not in source


def test_importlinter_lists_freight_term_on_deny() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.freight_term_marks" in forbidden
    assert "app.models.freight_term_mark" in forbidden


def test_api_types_include_freight_term_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "FreightTermMarkResponse" in source
    assert "FreightTermMarkCreate" in source


def test_fga_source_declares_freight_term_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_freight_term_marks: member" in source


def test_fga_model_grants_freight_term_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_freight_term_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitFreightTermAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryFreightTermDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[FreightTermMark] = []

    async def list_marks(self) -> list[FreightTermMark]:
        return list(self.rows)

    async def persist_freight_term_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        term_kind: object,
        source_ref: object,
    ) -> FreightTermMark:
        code, kind, origin = parse_freight_term_mark_row(
            mark_code,
            term_kind,
            source_ref,
        )
        row = FreightTermMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            term_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def freight_term_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryFreightTermDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.freight_term_marks.FreightTermMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitFreightTermAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "ftm_prepaid_01",
        "term_kind": "prepaid",
        "source_ref": "fixture://freight-term-mark/a",
    }
    body.update(extra)
    return body


def test_post_persists(freight_term_http: object) -> None:
    client, desk = freight_term_http
    response = client.post(
        "/api/v1/freight-term-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["term_kind"] == "prepaid"
    assert response.headers.get("X-Omni-Catalog") == "freight-term-mark"
    assert len(desk.rows) == 1


def test_post_rejects_amount_margin_score(freight_term_http: object) -> None:
    client, _desk = freight_term_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/freight-term-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_rejects_bad_code(freight_term_http: object) -> None:
    client, _desk = freight_term_http
    response = client.post(
        "/api/v1/freight-term-marks",
        headers=bearer_auth_headers(),
        json=_payload(mark_code="BAD"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_post_rejects_bad_kind(freight_term_http: object) -> None:
    client, _desk = freight_term_http
    response = client.post(
        "/api/v1/freight-term-marks",
        headers=bearer_auth_headers(),
        json=_payload(term_kind="collectible"),
    )
    assert response.status_code == 400
    assert "warunek frachtu" in response.json()["detail"]


def test_post_rejects_foreign_source_ref(freight_term_http: object) -> None:
    client, _desk = freight_term_http
    response = client.post(
        "/api/v1/freight-term-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_lists_rows(freight_term_http: object) -> None:
    client, desk = freight_term_http
    client.post(
        "/api/v1/freight-term-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/freight-term-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
