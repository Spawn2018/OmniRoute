from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.handover_sbar_mark import parse_handover_sbar_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.handover_sbar_mark import HandoverSbarMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount",)


def test_migration_419_creates_handover_sbar_mark_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/419_handover_sbar_mark.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "419_handover_sbar_mark"' in source
    assert 'down_revision: str | None = "418_shipment_clone_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "handover_sbar_mark_tenant_isolation" in source
    for banned in ("amount", "float(", "httpx", "auto_sbar", "chat"):
        assert banned not in source


def test_importlinter_lists_handover_sbar_mark_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.handover_sbar_marks" in forbidden
    assert "app.models.handover_sbar_mark" in forbidden


def test_fga_source_declares_handover_sbar_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_handover_sbar_marks: member" in source


def test_authorization_model_grants_handover_sbar_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_handover_sbar_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class HandoverSbarMarkAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryHandoverSbarMarkDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[HandoverSbarMark] = []

    async def list_marks(self) -> list[HandoverSbarMark]:
        return list(self.rows)

    async def persist_handover_sbar_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        sbar_kind: object,
        source_ref: object,
    ) -> HandoverSbarMark:
        code, kind, origin = parse_handover_sbar_mark_row(
            mark_code,
            sbar_kind,
            source_ref,
        )
        row = HandoverSbarMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            sbar_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def sbar_mark_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryHandoverSbarMarkDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.handover_sbar_marks.HandoverSbarMarkService",
        lambda _s: desk,
    )
    set_authz_checker(HandoverSbarMarkAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "sbar_sit_01",
        "sbar_kind": "situation",
        "source_ref": "fixture://handover-sbar-mark/a",
    }
    body.update(extra)
    return body


def test_post_handover_sbar_mark_persists(sbar_mark_http: object) -> None:
    client, desk = sbar_mark_http
    response = client.post(
        "/api/v1/handover-sbar-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["sbar_kind"] == "situation"
    assert len(desk.rows) == 1


def test_post_handover_sbar_mark_rejects_amount(sbar_mark_http: object) -> None:
    client, _desk = sbar_mark_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/handover-sbar-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_handover_sbar_mark_rejects_bad_kind(sbar_mark_http: object) -> None:
    client, _desk = sbar_mark_http
    response = client.post(
        "/api/v1/handover-sbar-marks",
        headers=bearer_auth_headers(),
        json=_payload(sbar_kind="auto_sbar"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_handover_sbar_mark_rejects_foreign_source_ref(
    sbar_mark_http: object,
) -> None:
    client, _desk = sbar_mark_http
    response = client.post(
        "/api/v1/handover-sbar-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_handover_sbar_marks_lists_rows(sbar_mark_http: object) -> None:
    client, desk = sbar_mark_http
    client.post(
        "/api/v1/handover-sbar-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/handover-sbar-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
