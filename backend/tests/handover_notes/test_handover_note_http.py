from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.handover_note import parse_handover_note_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.handover_note import HandoverNote
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount",)


def test_migration_424_creates_handover_note_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/424_handover_note.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "424_handover_note"' in source
    assert 'down_revision: str | None = "423_consignment_stop"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "handover_note_tenant_isolation" in source
    for banned in ("amount", "float(", "httpx", "auto_sbar", "chat"):
        assert banned not in source


def test_importlinter_lists_handover_note_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.handover_notes" in forbidden
    assert "app.models.handover_note" in forbidden


def test_fga_source_declares_handover_note_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_handover_notes: member" in source


def test_authorization_model_grants_handover_notes_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_handover_notes"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class HandoverNoteAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryHandoverNoteDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[HandoverNote] = []

    async def list_notes(self) -> list[HandoverNote]:
        return list(self.rows)

    async def persist_handover_note(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        note_code: object,
        situation: object,
        background: object,
        assessment: object,
        recommendation: object,
        source_ref: object,
    ) -> HandoverNote:
        code, sit, back, assess, rec, origin = parse_handover_note_row(
            note_code,
            situation,
            background,
            assessment,
            recommendation,
            source_ref,
        )
        row = HandoverNote(
            id=uuid4(),
            organization_id=organization_id,
            note_code=code,
            situation=sit,
            background=back,
            assessment=assess,
            recommendation=rec,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def note_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryHandoverNoteDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.handover_notes.HandoverNoteService",
        lambda _s: desk,
    )
    set_authz_checker(HandoverNoteAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "note_code": "shift_a_01",
        "situation": "brak kierowcy na PLGDY",
        "background": "urlop nagly",
        "assessment": "ryzyko opoznienia ETA",
        "recommendation": "przelozyc na jutro 06:00",
        "source_ref": "fixture://handover-note/a",
    }
    body.update(extra)
    return body


def test_post_handover_note_persists(note_http: object) -> None:
    client, desk = note_http
    response = client.post(
        "/api/v1/handover-notes",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["situation"] == "brak kierowcy na PLGDY"
    assert len(desk.rows) == 1


def test_post_handover_note_rejects_amount(note_http: object) -> None:
    client, _desk = note_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/handover-notes",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_handover_note_rejects_empty_situation(note_http: object) -> None:
    client, _desk = note_http
    response = client.post(
        "/api/v1/handover-notes",
        headers=bearer_auth_headers(),
        json=_payload(situation="  "),
    )
    assert response.status_code == 400
    assert "sytuacja" in response.json()["detail"]


def test_post_handover_note_rejects_foreign_source_ref(note_http: object) -> None:
    client, _desk = note_http
    response = client.post(
        "/api/v1/handover-notes",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_handover_notes_lists_rows(note_http: object) -> None:
    client, desk = note_http
    client.post(
        "/api/v1/handover-notes",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/handover-notes",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
