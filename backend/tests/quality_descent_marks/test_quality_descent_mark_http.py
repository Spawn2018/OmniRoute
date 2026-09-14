from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.quality_descent_mark import parse_quality_descent_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.quality_descent_mark import QualityDescentMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount",)


def test_migration_391_creates_quality_descent_mark_and_forces_rls() -> None:
    source = (
        _ROOT / "backend/alembic/versions/391_quality_descent_mark.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "391_quality_descent_mark"' in source
    assert 'down_revision: str | None = "390_style_fidelity_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "quality_descent_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "scoring"):
        assert banned not in source


def test_importlinter_lists_quality_descent_mark_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.quality_descent_marks" in forbidden
    assert "app.models.quality_descent_mark" in forbidden


def test_fga_source_declares_quality_descent_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_quality_descent_marks: member" in source


def test_authorization_model_grants_quality_descent_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_quality_descent_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class QualityDescentMarkAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryQualityDescentDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[QualityDescentMark] = []

    async def list_marks(self) -> list[QualityDescentMark]:
        return list(self.rows)

    async def persist_quality_descent_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        descent_kind: object,
        source_ref: object,
    ) -> QualityDescentMark:
        code, kind, origin = parse_quality_descent_mark_row(
            mark_code,
            descent_kind,
            source_ref,
        )
        row = QualityDescentMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            descent_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def quality_descent_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryQualityDescentDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.quality_descent_marks.QualityDescentMarkService",
        lambda _s: desk,
    )
    set_authz_checker(QualityDescentMarkAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "qd_mae_01",
        "descent_kind": "mae",
        "source_ref": "fixture://quality-descent/a",
    }
    body.update(extra)
    return body


def test_post_quality_descent_mark_persists(quality_descent_http: object) -> None:
    client, desk = quality_descent_http
    response = client.post(
        "/api/v1/quality-descent-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["descent_kind"] == "mae"
    assert len(desk.rows) == 1


def test_post_quality_descent_mark_rejects_amount(
    quality_descent_http: object,
) -> None:
    client, _desk = quality_descent_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/quality-descent-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_quality_descent_mark_rejects_bad_kind(
    quality_descent_http: object,
) -> None:
    client, _desk = quality_descent_http
    response = client.post(
        "/api/v1/quality-descent-marks",
        headers=bearer_auth_headers(),
        json=_payload(descent_kind="auto_drop"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_quality_descent_mark_rejects_foreign_source_ref(
    quality_descent_http: object,
) -> None:
    client, _desk = quality_descent_http
    response = client.post(
        "/api/v1/quality-descent-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_quality_descent_marks_lists_rows(
    quality_descent_http: object,
) -> None:
    client, desk = quality_descent_http
    client.post(
        "/api/v1/quality-descent-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/quality-descent-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
