from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.penalty_mark import parse_penalty_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.penalty_mark import PenaltyMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount", "penalty")


def test_migration_233_creates_penalty_mark_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/233_penalty_mark.py").read_text(encoding="utf-8")
    assert 'revision: str = "233_penalty_mark"' in source
    assert 'down_revision: str | None = "232_spend_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "penalty_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency", "penalty_amount"):
        assert banned not in source


def test_importlinter_lists_penalty_mark_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.penalty_marks" in forbidden
    assert "app.models.penalty_mark" in forbidden


def test_generated_api_types_include_penalty_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "PenaltyMarkResponse" in source
    assert "PenaltyMarkCreate" in source


def test_fga_source_declares_penalty_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_penalty_marks: member" in source


def test_authorization_model_grants_penalty_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_penalty_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitPenaltyAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryPenaltyDesk:
    def __init__(self, session: object) -> None:
        self.marks: list[PenaltyMark] = []

    async def list_marks(self) -> list[PenaltyMark]:
        return list(self.marks)

    async def persist_penalty_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        breach_kind: object,
        source_ref: object,
    ) -> PenaltyMark:
        code, kind, origin = parse_penalty_mark_row(mark_code, breach_kind, source_ref)
        row = PenaltyMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            breach_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.marks.append(row)
        return row


@pytest.fixture
def penalty_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryPenaltyDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.penalty_marks.PenaltyMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitPenaltyAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "otif_breach_01",
        "breach_kind": "otif",
        "source_ref": "fixture://penalty-mark/a",
    }
    body.update(extra)
    return body


def test_post_penalty_mark_persists(penalty_http: object) -> None:
    client, desk = penalty_http
    response = client.post(
        "/api/v1/penalty-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["breach_kind"] == "otif"
    assert len(desk.marks) == 1


def test_post_penalty_mark_rejects_amount_penalty(penalty_http: object) -> None:
    client, _desk = penalty_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/penalty-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_penalty_mark_rejects_bad_kind(penalty_http: object) -> None:
    client, _desk = penalty_http
    response = client.post(
        "/api/v1/penalty-marks",
        headers=bearer_auth_headers(),
        json=_payload(breach_kind="sql_kara"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_penalty_mark_rejects_foreign_source_ref(penalty_http: object) -> None:
    client, _desk = penalty_http
    response = client.post(
        "/api/v1/penalty-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_penalty_marks_lists_rows(penalty_http: object) -> None:
    client, desk = penalty_http
    client.post(
        "/api/v1/penalty-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/penalty-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.marks) == 1
