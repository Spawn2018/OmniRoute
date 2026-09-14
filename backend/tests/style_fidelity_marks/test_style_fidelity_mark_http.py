from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.style_fidelity_mark import parse_style_fidelity_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.style_fidelity_mark import StyleFidelityMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount",)


def test_migration_390_creates_style_fidelity_mark_and_forces_rls() -> None:
    source = (
        _ROOT / "backend/alembic/versions/390_style_fidelity_mark.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "390_style_fidelity_mark"' in source
    assert 'down_revision: str | None = "389_style_cascade_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "style_fidelity_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "scoring"):
        assert banned not in source


def test_importlinter_lists_style_fidelity_mark_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.style_fidelity_marks" in forbidden
    assert "app.models.style_fidelity_mark" in forbidden


def test_fga_source_declares_style_fidelity_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_style_fidelity_marks: member" in source


def test_authorization_model_grants_style_fidelity_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_style_fidelity_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class StyleFidelityMarkAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryStyleFidelityDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[StyleFidelityMark] = []

    async def list_marks(self) -> list[StyleFidelityMark]:
        return list(self.rows)

    async def persist_style_fidelity_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        fidelity_kind: object,
        source_ref: object,
    ) -> StyleFidelityMark:
        code, kind, origin = parse_style_fidelity_mark_row(
            mark_code,
            fidelity_kind,
            source_ref,
        )
        row = StyleFidelityMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            fidelity_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def style_fidelity_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryStyleFidelityDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.style_fidelity_marks.StyleFidelityMarkService",
        lambda _s: desk,
    )
    set_authz_checker(StyleFidelityMarkAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "fid_pass_01",
        "fidelity_kind": "pass",
        "source_ref": "fixture://style-fidelity/a",
    }
    body.update(extra)
    return body


def test_post_style_fidelity_mark_persists(style_fidelity_http: object) -> None:
    client, desk = style_fidelity_http
    response = client.post(
        "/api/v1/style-fidelity-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["fidelity_kind"] == "pass"
    assert len(desk.rows) == 1


def test_post_style_fidelity_mark_rejects_amount(
    style_fidelity_http: object,
) -> None:
    client, _desk = style_fidelity_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/style-fidelity-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_style_fidelity_mark_rejects_bad_kind(
    style_fidelity_http: object,
) -> None:
    client, _desk = style_fidelity_http
    response = client.post(
        "/api/v1/style-fidelity-marks",
        headers=bearer_auth_headers(),
        json=_payload(fidelity_kind="score_85"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_style_fidelity_mark_rejects_foreign_source_ref(
    style_fidelity_http: object,
) -> None:
    client, _desk = style_fidelity_http
    response = client.post(
        "/api/v1/style-fidelity-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_style_fidelity_marks_lists_rows(style_fidelity_http: object) -> None:
    client, desk = style_fidelity_http
    client.post(
        "/api/v1/style-fidelity-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/style-fidelity-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
