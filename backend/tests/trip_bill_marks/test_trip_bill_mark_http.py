from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.trip_bill_mark import parse_trip_bill_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.trip_bill_mark import TripBillMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount",)


def test_migration_420_creates_trip_bill_mark_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/420_trip_bill_mark.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "420_trip_bill_mark"' in source
    assert 'down_revision: str | None = "419_handover_sbar_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "trip_bill_mark_tenant_isolation" in source
    for banned in ("amount", "float(", "httpx", "trips_to_bill", "ksef"):
        assert banned not in source


def test_importlinter_lists_trip_bill_mark_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.trip_bill_marks" in forbidden
    assert "app.models.trip_bill_mark" in forbidden


def test_fga_source_declares_trip_bill_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_trip_bill_marks: member" in source


def test_authorization_model_grants_trip_bill_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_trip_bill_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class TripBillMarkAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryTripBillMarkDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[TripBillMark] = []

    async def list_marks(self) -> list[TripBillMark]:
        return list(self.rows)

    async def persist_trip_bill_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        bill_kind: object,
        source_ref: object,
    ) -> TripBillMark:
        code, kind, origin = parse_trip_bill_mark_row(
            mark_code,
            bill_kind,
            source_ref,
        )
        row = TripBillMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            bill_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def trip_bill_mark_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryTripBillMarkDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.trip_bill_marks.TripBillMarkService",
        lambda _s: desk,
    )
    set_authz_checker(TripBillMarkAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "bill_ready_01",
        "bill_kind": "ready",
        "source_ref": "fixture://trip-bill-mark/a",
    }
    body.update(extra)
    return body


def test_post_trip_bill_mark_persists(trip_bill_mark_http: object) -> None:
    client, desk = trip_bill_mark_http
    response = client.post(
        "/api/v1/trip-bill-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["bill_kind"] == "ready"
    assert len(desk.rows) == 1


def test_post_trip_bill_mark_rejects_amount(trip_bill_mark_http: object) -> None:
    client, _desk = trip_bill_mark_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/trip-bill-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_trip_bill_mark_rejects_bad_kind(trip_bill_mark_http: object) -> None:
    client, _desk = trip_bill_mark_http
    response = client.post(
        "/api/v1/trip-bill-marks",
        headers=bearer_auth_headers(),
        json=_payload(bill_kind="trips_to_bill"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_trip_bill_mark_rejects_foreign_source_ref(
    trip_bill_mark_http: object,
) -> None:
    client, _desk = trip_bill_mark_http
    response = client.post(
        "/api/v1/trip-bill-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_trip_bill_marks_lists_rows(trip_bill_mark_http: object) -> None:
    client, desk = trip_bill_mark_http
    client.post(
        "/api/v1/trip-bill-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/trip-bill-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
