from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.capa_mark import parse_capa_mark_row
from app.main import app
from app.models.capa_mark import CapaMark
from tests.http_auth import bearer_auth_headers

_FORBIDDEN = ("shipment_id", "amount", "workflow_id", "currency")


class PermitCapaMarkAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryCapaMarkDesk:
    def __init__(self, session: object) -> None:
        self._session = session
        self.marks: list[CapaMark] = []

    async def list_marks(self) -> list[CapaMark]:
        return list(self.marks)

    async def persist_capa_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        mark_kind: object,
        source_ref: object,
    ) -> CapaMark:
        code, scope, origin = parse_capa_mark_row(mark_code, mark_kind, source_ref)
        row = CapaMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            mark_kind=scope,
            source_ref=origin,
            created_by=user_id,
        )
        self.marks.append(row)
        return row


@pytest.fixture
def capa_mark_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryCapaMarkDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr("app.api.capa_marks.CapaMarkService", lambda _s: desk)
    set_authz_checker(PermitCapaMarkAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "capa_pl_01",
        "mark_kind": "capa",
        "source_ref": "fixture://capa-mark/pl-1",
    }
    body.update(extra)
    return body


def test_http_lists_and_creates_capa_mark(capa_mark_http: object) -> None:
    client, _desk = capa_mark_http
    created = client.post(
        "/api/v1/capa-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert created.status_code == 201
    assert created.json()["mark_kind"] == "capa"
    listed = client.get("/api/v1/capa-marks", headers=bearer_auth_headers())
    assert listed.status_code == 200
    assert len(listed.json()) == 1


def test_http_rejects_bad_mark_code(capa_mark_http: object) -> None:
    client, _desk = capa_mark_http
    response = client.post(
        "/api/v1/capa-marks",
        headers=bearer_auth_headers(),
        json=_payload(mark_code="X"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_http_rejects_bad_kind(capa_mark_http: object) -> None:
    client, _desk = capa_mark_http
    response = client.post(
        "/api/v1/capa-marks",
        headers=bearer_auth_headers(),
        json=_payload(mark_kind="workflow"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


@pytest.mark.parametrize("field", _FORBIDDEN)
def test_http_forbids_shipment_and_metric_fields(
    capa_mark_http: object, field: str
) -> None:
    client, _desk = capa_mark_http
    body = _payload()
    body[field] = "x"
    response = client.post(
        "/api/v1/capa-marks",
        headers=bearer_auth_headers(),
        json=body,
    )
    assert response.status_code == 422
