from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.slot_guarantee_mark import parse_slot_guarantee_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.slot_guarantee_mark import SlotGuaranteeMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]

_FORBIDDEN = ("amount", "margin", "confirmed")


def test_migration_329_creates_slot_guarantee_and_rls() -> None:
    source = (
        _ROOT / "backend/alembic/versions/329_slot_guarantee_mark.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "329_slot_guarantee_mark"' in source
    assert 'down_revision: str | None = "328_named_place_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "slot_guarantee_mark_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency"):
        assert banned not in source.lower()
    assert 'sa.Column("amount"' not in source
    assert 'sa.Column("confirmed"' not in source


def test_importlinter_lists_slot_guarantee_on_deny() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.slot_guarantee_marks" in forbidden
    assert "app.models.slot_guarantee_mark" in forbidden


def test_api_types_include_slot_guarantee_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "SlotGuaranteeMarkResponse" in source
    assert "SlotGuaranteeMarkCreate" in source


def test_fga_source_declares_slot_guarantee_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_slot_guarantee_marks: member" in source


def test_fga_model_grants_slot_guarantee_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_slot_guarantee_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitSlotGuaranteeAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemorySlotGuaranteeDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[SlotGuaranteeMark] = []

    async def list_marks(self) -> list[SlotGuaranteeMark]:
        return list(self.rows)

    async def persist_slot_guarantee_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        stance_kind: object,
        source_ref: object,
    ) -> SlotGuaranteeMark:
        code, kind, origin = parse_slot_guarantee_mark_row(
            mark_code,
            stance_kind,
            source_ref,
        )
        row = SlotGuaranteeMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            stance_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def slot_guarantee_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemorySlotGuaranteeDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.slot_guarantee_marks.SlotGuaranteeMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitSlotGuaranteeAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "sgm_cap_01",
        "stance_kind": "capability",
        "source_ref": "fixture://slot-guarantee-mark/a",
    }
    body.update(extra)
    return body


def test_post_persists(slot_guarantee_http: object) -> None:
    client, desk = slot_guarantee_http
    response = client.post(
        "/api/v1/slot-guarantee-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["stance_kind"] == "capability"
    assert response.headers.get("X-Omni-Catalog") == "slot-guarantee-mark"
    assert len(desk.rows) == 1


def test_post_rejects_amount_margin_confirmed(slot_guarantee_http: object) -> None:
    client, _desk = slot_guarantee_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/slot-guarantee-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_rejects_bad_code(slot_guarantee_http: object) -> None:
    client, _desk = slot_guarantee_http
    response = client.post(
        "/api/v1/slot-guarantee-marks",
        headers=bearer_auth_headers(),
        json=_payload(mark_code="BAD"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_post_rejects_bad_kind(slot_guarantee_http: object) -> None:
    client, _desk = slot_guarantee_http
    response = client.post(
        "/api/v1/slot-guarantee-marks",
        headers=bearer_auth_headers(),
        json=_payload(stance_kind="binding"),
    )
    assert response.status_code == 400
    assert "postawa" in response.json()["detail"]


def test_post_rejects_foreign_source_ref(slot_guarantee_http: object) -> None:
    client, _desk = slot_guarantee_http
    response = client.post(
        "/api/v1/slot-guarantee-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_lists_rows(slot_guarantee_http: object) -> None:
    client, desk = slot_guarantee_http
    client.post(
        "/api/v1/slot-guarantee-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/slot-guarantee-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
