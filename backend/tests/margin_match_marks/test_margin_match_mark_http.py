from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.margin_match_mark import parse_margin_match_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.margin_match_mark import MarginMatchMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "margin")


def test_migration_511_creates_margin_match_mark_and_forces_rls() -> None:
    source = (
        _ROOT / "backend/alembic/versions/511_margin_match_mark.py"
    ).read_text(encoding="utf-8-sig")
    assert 'revision: str = "511_margin_match_mark"' in source
    assert 'down_revision: str | None = "510_trip_variance_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "margin_match_mark_tenant_isolation" in source
    for banned in ("amount", "float(", "httpx", "currency"):
        assert banned not in source


def test_importlinter_lists_margin_match_marks_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.margin_match_marks" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.margin_match_marks" in forbidden
    assert "app.models.margin_match_mark" in forbidden


def test_fga_source_declares_margin_match_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_margin_match_marks: member" in source


def test_authorization_model_grants_margin_match_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_margin_match_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


def test_generated_api_types_include_margin_match_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "MarginMatchMarkResponse" in source
    assert "MarginMatchMarkCreate" in source


def test_agents_forbids_trip_import() -> None:
    agents = (
        _ROOT / "backend/app/services/margin_match_marks/AGENTS.md"
    ).read_text(encoding="utf-8")
    assert "trips" in agents
    assert "UPDATE / DELETE" in agents or "UPDATE / DELETE wiersza" in agents


def test_service_file_avoids_trip_import() -> None:
    source = (
        _ROOT
        / "backend/app/services/margin_match_marks"
        / "margin_match_mark_service.py"
    ).read_text(encoding="utf-8")
    assert "trips" not in source
    assert "charges" not in source


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
        self.rows: list[MarginMatchMark] = []

    async def list_marks(self) -> list[MarginMatchMark]:
        return list(self.rows)

    async def persist_margin_match_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        match_kind: object,
        source_ref: object,
    ) -> MarginMatchMark:
        code, kind, origin = parse_margin_match_mark_row(
            mark_code,
            match_kind,
            source_ref,
        )
        row = MarginMatchMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            match_kind=kind,
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
        "app.api.margin_match_marks.MarginMatchMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitMarkAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "var_match_01",
        "match_kind": "match",
        "source_ref": "fixture://margin-match/a",
    }
    body.update(extra)
    return body


def test_post_margin_match_mark_persists(mark_http: object) -> None:
    client, desk = mark_http
    response = client.post(
        "/api/v1/margin-match-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["match_kind"] == "match"
    assert len(desk.rows) == 1


def test_post_margin_match_mark_rejects_bad_kind(mark_http: object) -> None:
    client, _desk = mark_http
    response = client.post(
        "/api/v1/margin-match-marks",
        headers=bearer_auth_headers(),
        json=_payload(match_kind="live"),
    )
    assert response.status_code == 400
    assert "dopasowanie" in response.json()["detail"]


def test_post_margin_match_mark_rejects_amount(mark_http: object) -> None:
    client, _desk = mark_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/margin-match-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_get_margin_match_marks_lists(mark_http: object) -> None:
    client, desk = mark_http
    client.post(
        "/api/v1/margin-match-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/margin-match-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
