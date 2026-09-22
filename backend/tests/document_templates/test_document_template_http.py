from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.document_template import (
    require_branding_ref,
    require_layout_ref,
    require_output_kind,
    require_template_kind,
    require_template_language,
    require_template_source_ref,
)
from app.main import app
from app.models.document_template import DocumentTemplate
from tests.http_auth import bearer_auth_headers


class AllowAllAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class StubDocumentTemplateService:
    def __init__(self, session: object) -> None:
        self._session = session
        self.rows: list[DocumentTemplate] = []

    async def list_templates(self) -> list[DocumentTemplate]:
        return list(self.rows)

    async def record_template(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        template_kind: str,
        language: str,
        layout_ref: str,
        output_kind: str,
        source_ref: str,
        branding_ref: str | None = None,
    ) -> DocumentTemplate:
        row = DocumentTemplate(
            id=uuid4(),
            organization_id=organization_id,
            template_kind=require_template_kind(template_kind),
            language=require_template_language(language),
            layout_ref=require_layout_ref(layout_ref),
            branding_ref=require_branding_ref(branding_ref),
            output_kind=require_output_kind(output_kind),
            source_ref=require_template_source_ref(source_ref),
            created_by=user_id,
        )
        self.rows.append(row)
        return row


@pytest.fixture
def catalog_client(monkeypatch: pytest.MonkeyPatch) -> object:
    rows = StubDocumentTemplateService(object())

    def _rows(_session: object) -> StubDocumentTemplateService:
        return rows

    async def _fake_tenant_session() -> object:
        session = AsyncMock()
        session.commit = AsyncMock()
        return session

    monkeypatch.setattr(
        "app.api.document_templates.DocumentTemplateService",
        _rows,
    )
    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app), rows
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _payload(**overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "template_kind": "own_label",
        "language": "pl",
        "layout_ref": "own-label-pl",
        "output_kind": "html_print",
        "source_ref": "fixture://document-template/1",
    }
    body.update(overrides)
    return body


def test_http_create_and_list_document_template(catalog_client: object) -> None:
    client, _rows = catalog_client
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post(
        "/api/v1/document-templates",
        headers=headers,
        json=_payload(),
    )
    assert created.status_code == 201
    body = created.json()
    assert body["organization_id"] == str(org_id)
    assert body["template_kind"] == "own_label"
    assert body["layout_ref"] == "own-label-pl"
    assert body["branding_ref"] is None
    assert body["output_kind"] == "html_print"
    assert "amount" not in body
    assert "buy_amount" not in body
    listed = client.get("/api/v1/document-templates", headers=headers)
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == body["id"]


def test_http_create_template_with_branding_ref(catalog_client: object) -> None:
    client, _rows = catalog_client
    created = client.post(
        "/api/v1/document-templates",
        headers=bearer_auth_headers(),
        json=_payload(branding_ref="tenant-logo"),
    )
    assert created.status_code == 201
    assert created.json()["branding_ref"] == "tenant-logo"


def test_http_create_template_bad_branding_is_400(catalog_client: object) -> None:
    client, _rows = catalog_client
    response = client.post(
        "/api/v1/document-templates",
        headers=bearer_auth_headers(),
        json=_payload(branding_ref="Own Brand"),
    )
    assert response.status_code == 400
    assert "branding" in response.json()["detail"]


def test_http_create_template_unknown_kind_is_400(catalog_client: object) -> None:
    client, _rows = catalog_client
    response = client.post(
        "/api/v1/document-templates",
        headers=bearer_auth_headers(),
        json=_payload(template_kind="network_label"),
    )
    assert response.status_code == 400
    assert "rodzaj" in response.json()["detail"]


def test_http_create_template_bad_layout_is_400(catalog_client: object) -> None:
    client, _rows = catalog_client
    response = client.post(
        "/api/v1/document-templates",
        headers=bearer_auth_headers(),
        json=_payload(layout_ref="Own Label"),
    )
    assert response.status_code == 400
    assert "układ" in response.json()["detail"]


def test_http_create_template_unknown_language_is_400(catalog_client: object) -> None:
    client, _rows = catalog_client
    response = client.post(
        "/api/v1/document-templates",
        headers=bearer_auth_headers(),
        json=_payload(language="de"),
    )
    assert response.status_code == 400
    assert "język" in response.json()["detail"]


def test_http_create_template_unknown_output_is_400(catalog_client: object) -> None:
    client, _rows = catalog_client
    response = client.post(
        "/api/v1/document-templates",
        headers=bearer_auth_headers(),
        json=_payload(output_kind="pdf"),
    )
    assert response.status_code == 400
    assert "wyjście" in response.json()["detail"]


def test_http_create_template_foreign_source_ref_is_400(catalog_client: object) -> None:
    client, _rows = catalog_client
    response = client.post(
        "/api/v1/document-templates",
        headers=bearer_auth_headers(),
        json=_payload(source_ref="http://hold.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]
