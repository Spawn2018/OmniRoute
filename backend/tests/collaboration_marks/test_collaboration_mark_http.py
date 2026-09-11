from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.collaboration_mark import parse_collaboration_mark_row
from app.main import app
from app.models.collaboration_mark import CollaborationMark
from tests.http_auth import bearer_auth_headers

_FORBIDDEN = ("amount", "margin", "shipment_id", "party_id")


class PermitCollabAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryCollabDesk:
    def __init__(self, session: object) -> None:
        self.marks: list[CollaborationMark] = []

    async def list_marks(self) -> list[CollaborationMark]:
        return list(self.marks)

    async def persist_collaboration_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        role_kind: object,
        source_ref: object,
    ) -> CollaborationMark:
        code, kind, origin = parse_collaboration_mark_row(
            mark_code, role_kind, source_ref
        )
        row = CollaborationMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            role_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.marks.append(row)
        return row


@pytest.fixture
def collab_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryCollabDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.collaboration_marks.CollaborationMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitCollabAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "seat_shipper_01",
        "role_kind": "shipper",
        "source_ref": "fixture://collaboration-mark/pl-1",
    }
    body.update(extra)
    return body


def test_http_lists_and_creates_collaboration_mark(collab_http: object) -> None:
    client, _desk = collab_http
    created = client.post(
        "/api/v1/collaboration-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert created.status_code == 201
    listed = client.get(
        "/api/v1/collaboration-marks",
        headers=bearer_auth_headers(),
    )
    assert listed.status_code == 200
    assert len(listed.json()) == 1


@pytest.mark.parametrize("field", _FORBIDDEN)
def test_http_forbids_money_and_party_fields(collab_http: object, field: str) -> None:
    client, _desk = collab_http
    body = _payload()
    body[field] = "x"
    response = client.post(
        "/api/v1/collaboration-marks",
        headers=bearer_auth_headers(),
        json=body,
    )
    assert response.status_code == 422
