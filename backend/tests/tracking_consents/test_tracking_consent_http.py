from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.tracking_consent import parse_tracking_consent_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.tracking_consent import TrackingConsent
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_FORBIDDEN = ("amount",)


def test_migration_364_creates_tracking_consent_and_forces_rls() -> None:
    source = (_ROOT / "backend/alembic/versions/364_tracking_consent.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "364_tracking_consent"' in source
    assert 'down_revision: str | None = "363_telematics_device"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "tracking_consent_tenant_isolation" in source
    for banned in ("amount", "margin", "float(", "httpx", "currency"):
        assert banned not in source


def test_importlinter_lists_tracking_consent_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.tracking_consents" in forbidden
    assert "app.models.tracking_consent" in forbidden


def test_fga_source_declares_tracking_consent_relation() -> None:
    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")
    assert "can_manage_tracking_consents: member" in source


def test_authorization_model_grants_tracking_consents_to_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_tracking_consents"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


class PermitConsentAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryConsentDesk:
    def __init__(self, session: object) -> None:
        self.rows: list[TrackingConsent] = []

    async def list_consents(self) -> list[TrackingConsent]:
        return list(self.rows)

    async def persist_tracking_consent(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        consent_code: object,
        consent_kind: object,
        source_ref: object,
    ) -> TrackingConsent:
        code, kind, origin = parse_tracking_consent_row(
            consent_code,
            consent_kind,
            source_ref,
        )
        row = TrackingConsent(
            id=uuid4(),
            organization_id=organization_id,
            consent_code=code,
            consent_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def consent_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryConsentDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.tracking_consents.TrackingConsentService",
        lambda _s: desk,
    )
    set_authz_checker(PermitConsentAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**extra: object) -> dict[str, object]:
    body: dict[str, object] = {
        "consent_code": "cns_party_01",
        "consent_kind": "party",
        "source_ref": "fixture://tracking-consent/a",
    }
    body.update(extra)
    return body


def test_post_tracking_consent_persists(consent_http: object) -> None:
    client, desk = consent_http
    response = client.post(
        "/api/v1/tracking-consents",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    assert response.status_code == 201
    assert response.json()["consent_kind"] == "party"
    assert len(desk.rows) == 1


def test_post_tracking_consent_rejects_amount(consent_http: object) -> None:
    client, _desk = consent_http
    for field in _FORBIDDEN:
        response = client.post(
            "/api/v1/tracking-consents",
            headers=bearer_auth_headers(),
            json=_payload(**{field: "x"}),
        )
        assert response.status_code == 422, field


def test_post_tracking_consent_rejects_bad_kind(consent_http: object) -> None:
    client, _desk = consent_http
    response = client.post(
        "/api/v1/tracking-consents",
        headers=bearer_auth_headers(),
        json=_payload(consent_kind="poll"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_post_tracking_consent_rejects_foreign_source_ref(
    consent_http: object,
) -> None:
    client, _desk = consent_http
    response = client.post(
        "/api/v1/tracking-consents",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://evil.example/x"),
    )
    assert response.status_code == 400
    assert "wskazanie" in response.json()["detail"]


def test_get_tracking_consents_lists_rows(consent_http: object) -> None:
    client, desk = consent_http
    client.post(
        "/api/v1/tracking-consents",
        headers=bearer_auth_headers(),
        json=_payload(),
    )
    response = client.get(
        "/api/v1/tracking-consents",
        headers=bearer_auth_headers(),
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert len(desk.rows) == 1
