from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.calibration_mark import parse_calibration_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.calibration_mark import CalibrationMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("shipment_id", "amount", "mae", "currency")


def test_migration_230_creates_calibration_mark_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/230_calibration_mark.py").read_text(
        encoding="utf-8"
    )
    assert 'revision: str = "230_calibration_mark"' in source
    assert 'down_revision: str | None = "229_clause_notice"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "calibration_mark_tenant_isolation" in source
    for banned in ("mae", "amount", "float(", "httpx", "currency"):
        assert banned not in source


def test_importlinter_lists_calibration_mark_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.calibration_marks" in forbidden
    assert "app.models.calibration_mark" in forbidden


def test_generated_api_types_include_calibration_mark() -> None:
    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "CalibrationMarkResponse" in source
    assert "CalibrationMarkCreate" in source


def test_fga_source_declares_calibration_mark_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_calibration_marks: member" in source


def test_authorization_model_grants_calibration_marks_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_calibration_marks"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitCalibrationAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryCalibrationDesk:
    def __init__(self, session: object) -> None:
        self.marks: list[CalibrationMark] = []

    async def list_marks(self) -> list[CalibrationMark]:
        return list(self.marks)

    async def persist_calibration_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        sample_ready: object,
        source_ref: object,
    ) -> CalibrationMark:
        code, ready, origin = parse_calibration_mark_row(
            mark_code, sample_ready, source_ref
        )
        row = CalibrationMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            sample_ready=ready,
            source_ref=origin,
            created_by=user_id,
        )
        self.marks.append(row)
        return row


@pytest.fixture
def calibration_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryCalibrationDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.calibration_marks.CalibrationMarkService",
        lambda _s: desk,
    )
    set_authz_checker(PermitCalibrationAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "mark_code": "sample_pl_01",
        "sample_ready": "ready",
        "source_ref": "fixture://calibration-mark/a",
    }
    body.update(extra)
    return body


def test_post_calibration_mark_persists(calibration_http: object) -> None:
    client, desk = calibration_http
    response = client.post(
        "/api/v1/calibration-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["sample_ready"] == "ready"
    assert len(desk.marks) == 1


def test_post_calibration_mark_rejects_extra(calibration_http: object) -> None:
    client, _desk = calibration_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/calibration-marks",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_calibration_mark_rejects_bad_kind(calibration_http: object) -> None:
    client, _desk = calibration_http
    response = client.post(
        "/api/v1/calibration-marks",
        headers=bearer_auth_headers(),
        json=_payload(sample_ready="mae"),
    )
    assert response.status_code == 400
    assert "gotowość" in response.json()["detail"]


def test_post_calibration_mark_rejects_foreign_source_ref(
    calibration_http: object,
) -> None:
    client, _desk = calibration_http
    response = client.post(
        "/api/v1/calibration-marks",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_calibration_marks_lists_rows(calibration_http: object) -> None:
    client, desk = calibration_http
    client.post(
        "/api/v1/calibration-marks",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/calibration-marks",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.marks) == 1
