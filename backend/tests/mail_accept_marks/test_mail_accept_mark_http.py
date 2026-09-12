from pathlib import Path
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.mail_accept_mark import parse_mail_accept_mark_row
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from app.models.mail_accept_mark import MailAcceptMark
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]

_FORBIDDEN = ("amount", "bytes")

def test_migration_305_creates_mail_accept_and_rls() -> None:

    source = (_ROOT / "backend/alembic/versions/305_mail_accept_mark.py").read_text(

        encoding="utf-8",

    )

    assert 'revision: str = "305_mail_accept_mark"' in source

    assert 'down_revision: str | None = "304_terms_ai_mark"' in source

    assert "FORCE ROW LEVEL SECURITY" in source

    assert "mail_accept_mark_tenant_isolation" in source

    for banned in ("amount", "margin", "float(", "httpx", "currency", "bytes"):

        assert banned not in source

def test_importlinter_lists_terms_ai_on_deny() -> None:

    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")

    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]

    assert "app.services.mail_accept_marks" in forbidden

    assert "app.models.mail_accept_mark" in forbidden

def test_api_types_include_mail_accept_mark() -> None:

    source = (_ROOT / "frontend/src/api/types.gen.ts").read_text(encoding="utf-8")

    assert "MailAcceptMarkResponse" in source

    assert "MailAcceptMarkCreate" in source

def test_fga_source_declares_ab_sus_relation() -> None:

    source = (_ROOT / "authz/model.fga").read_text(encoding="utf-8")

    assert "can_manage_mail_accept_marks: member" in source

def test_fga_model_grants_ab_sus_to_member() -> None:

    organization = next(

        definition

        for definition in authorization_model_request().type_definitions

        if definition.type == "organization"

    )

    relation = organization.relations["can_manage_mail_accept_marks"]

    assert relation.computed_userset is not None

    assert relation.computed_userset.relation == "member"

class PermitTermsAiAuthz:

    async def check(

        self,

        *,

        user_id: UUID,

        relation: str,

        object_type: str,

        object_id: UUID,

    ) -> bool:

        return True

class InMemoryFleetCostDesk:

    def __init__(self, session: object) -> None:

        self.rows: list[MailAcceptMark] = []

    async def list_marks(self) -> list[MailAcceptMark]:

        return list(self.rows)

    async def persist_mail_accept_mark(

        self,

        *,

        organization_id: UUID,

        user_id: UUID,

        mark_code: object,

        accept_kind: object,

        source_ref: object,

    ) -> MailAcceptMark:

        code, kind, origin = parse_mail_accept_mark_row(

            mark_code,

            accept_kind,

            source_ref,

        )

        row = MailAcceptMark(

            id=uuid4(),

            organization_id=organization_id,

            mark_code=code,

            accept_kind=kind,

            source_ref=origin,

            created_by=user_id,

        )

        self.rows.append(row)

        return row

@pytest.fixture

def terms_ai_http(monkeypatch: pytest.MonkeyPatch) -> object:

    desk = InMemoryFleetCostDesk(object())

    async def _session() -> object:

        handle = AsyncMock()

        handle.commit = AsyncMock()

        return handle

    monkeypatch.setattr(

        "app.api.mail_accept_marks.MailAcceptMarkService",

        lambda _s: desk,

    )

    set_authz_checker(PermitTermsAiAuthz())

    app.dependency_overrides[require_tenant_session] = _session

    yield TestClient(app), desk

    app.dependency_overrides.clear()

    set_authz_checker(None)

def _payload(**extra: object) -> dict[str, object]:

    body: dict[str, object] = {

        "mark_code": "mac_mailto_01",

        "accept_kind": "mailto",

        "source_ref": "fixture://mail-accept-mark/a",

    }

    body.update(extra)

    return body

def test_post_persists(terms_ai_http: object) -> None:

    client, desk = terms_ai_http

    response = client.post(

        "/api/v1/mail-accept-marks",

        headers=bearer_auth_headers(),

        json=_payload(),

    )

    assert response.status_code == 201

    assert response.json()["accept_kind"] == "mailto"

    assert len(desk.rows) == 1

def test_post_rejects_amount_bytes(terms_ai_http: object) -> None:

    client, _desk = terms_ai_http

    for field in _FORBIDDEN:

        response = client.post(

            "/api/v1/mail-accept-marks",

            headers=bearer_auth_headers(),

            json=_payload(**{field: "x"}),

        )

        assert response.status_code == 422, field

def test_post_rejects_bad_code(terms_ai_http: object) -> None:

    client, _desk = terms_ai_http

    response = client.post(

        "/api/v1/mail-accept-marks",

        headers=bearer_auth_headers(),

        json=_payload(mark_code="BAD"),

    )

    assert response.status_code == 400

    assert "oznaczenie" in response.json()["detail"]

def test_post_rejects_bad_kind(terms_ai_http: object) -> None:

    client, _desk = terms_ai_http

    response = client.post(

        "/api/v1/mail-accept-marks",

        headers=bearer_auth_headers(),

        json=_payload(accept_kind="live_terms"),

    )

    assert response.status_code == 400

    assert "rodzaj" in response.json()["detail"]

def test_post_rejects_foreign_source_ref(terms_ai_http: object) -> None:

    client, _desk = terms_ai_http

    response = client.post(

        "/api/v1/mail-accept-marks",

        headers=bearer_auth_headers(),

        json=_payload(source_ref="http://evil.example/x"),

    )

    assert response.status_code == 400

    assert "wskazanie" in response.json()["detail"]

def test_get_lists_rows(terms_ai_http: object) -> None:

    client, desk = terms_ai_http

    client.post(

        "/api/v1/mail-accept-marks",

        headers=bearer_auth_headers(),

        json=_payload(),

    )

    response = client.get(

        "/api/v1/mail-accept-marks",

        headers=bearer_auth_headers(),

    )

    assert response.status_code == 200

    assert len(response.json()) == 1

    assert len(desk.rows) == 1

