from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.named_place_mark import parse_named_place_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.named_place_mark import NamedPlaceMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]

_FORBIDDEN = ("amount", "margin", "icc_quote")


def test_migration_328_creates_named_place_and_rls() -> None:
    source = (
        _ROOT / "backend/alembic/versions/328_named_place_mark.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "328_named_place_mark"' in source
    assert 'down_revision: str | None = "327_dual_ledger_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "named_place_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency"):
        assert banned not in source.lower()
    assert 'sa.Column("amount"' not in source
    assert 'sa.Column("margin"' not in source
    assert 'sa.Column("icc_quote"' not in source
    assert "icc_quote" not in source.lower()


def test_importlinter_lists_named_place_on_deny() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.named_place_marks" in forbidden
    assert "app.models.named_place_mark" in forbidden


def test_api_types_include_named_place_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "NamedPlaceMarkResponse" in source
    assert "NamedPlaceMarkCreate" in source


def test_fga_source_declares_named_place_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_named_place_marks: member" in source


def test_fga_model_grants_named_place_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_named_place_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitNamedPlaceAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryNamedPlaceDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[NamedPlaceMark] = []

    async def list_marks(self) -> list[NamedPlaceMark]:
        return list(self.rows)

    async def persist_named_place_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        named_place: object,
        terms_version: object,
        source_ref: object,
    ) -> NamedPlaceMark:
        code, place, version, origin = parse_named_place_mark_row(
            mark_code,
            named_place,
            terms_version,
            source_ref,
        )
        row = NamedPlaceMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            named_place=place,
            terms_version=version,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def named_place_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryNamedPlaceDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.named_place_marks.NamedPlaceMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitNamedPlaceAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "npm_dap_waw",
        "named_place": "Warszawa",
        "terms_version": "2020",
        "source_ref": "fixture://named-place-mark/a",
    }
    body.update(extra)
    return body


def test_post_persists(named_place_http: object) -> None:
    client, desk = named_place_http
    response = client.post(
        "/api/v1/named-place-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["named_place"] == "Warszawa"
    assert response.json()["terms_version"] == "2020"
    assert response.headers.get("X-Omni-Catalog") == "named-place-mark"
    assert len(desk.rows) == 1


def test_post_rejects_amount_margin_icc_quote(named_place_http: object) -> None:
    client, _desk = named_place_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/named-place-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_rejects_bad_code(named_place_http: object) -> None:
    client, _desk = named_place_http
    response = client.post(
        "/api/v1/named-place-marks",
        headers=bearer_auth_headers(),
        json=_payload(mark_code="BAD"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_post_rejects_bad_version(named_place_http: object) -> None:
    client, _desk = named_place_http
    response = client.post(
        "/api/v1/named-place-marks",
        headers=bearer_auth_headers(),
        json=_payload(terms_version="2000"),
    )
    assert response.status_code == 400
    assert "wersja" in response.json()["detail"]


def test_post_rejects_foreign_source_ref(named_place_http: object) -> None:
    client, _desk = named_place_http
    response = client.post(
        "/api/v1/named-place-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_lists_rows(named_place_http: object) -> None:
    client, desk = named_place_http
    client.post(
        "/api/v1/named-place-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/named-place-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
