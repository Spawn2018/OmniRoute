import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.api.deps import require_tenant_session, set_authz_checker
from app.api.extractions import DOCUMENT_BASE64_MAX_LENGTH, ExtractRequest
from app.main import app
from tests.http_auth import bearer_auth_headers


class AllowAllAuthz:
    async def check(self, *, user_id, relation, object_type, object_id) -> bool:
        return True


@pytest.fixture
def xor_client():
    async def _fake_tenant_session():
        return object()

    set_authz_checker(AllowAllAuthz())
    app.dependency_overrides[require_tenant_session] = _fake_tenant_session
    yield TestClient(app)
    app.dependency_overrides.clear()
    set_authz_checker(None)


def test_extract_request_rejects_both_sources() -> None:
    with pytest.raises(ValidationError):
        ExtractRequest(source_ref="doc://x", input_text="THC 1 EUR", document_base64="YQ==")


def test_extract_request_rejects_neither_source() -> None:
    with pytest.raises(ValidationError):
        ExtractRequest(source_ref="doc://x")


def test_http_extract_rejects_both_sources(xor_client: TestClient) -> None:
    response = xor_client.post(
        "/api/v1/extractions",
        headers=bearer_auth_headers(),
        json={
            "source_ref": "doc://x",
            "input_text": "THC 1 EUR",
            "document_base64": "YQ==",
        },
    )
    assert response.status_code == 422


def test_http_extract_rejects_neither_source(xor_client: TestClient) -> None:
    response = xor_client.post(
        "/api/v1/extractions",
        headers=bearer_auth_headers(),
        json={"source_ref": "doc://x"},
    )
    assert response.status_code == 422


def test_extract_request_rejects_oversized_document_base64() -> None:
    oversized = "A" * (DOCUMENT_BASE64_MAX_LENGTH + 1)
    with pytest.raises(ValidationError):
        ExtractRequest(source_ref="doc://x", document_base64=oversized)


def test_http_extract_oversized_document_base64_is_422_before_decode(
    xor_client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    decode_calls: list[str] = []

    def _forbidden_decode(payload: str, validate: bool = False) -> bytes:
        decode_calls.append(payload)
        raise AssertionError("b64decode nie wolno wołać przed odrzuceniem max_length")

    monkeypatch.setattr("app.api.extractions.b64decode", _forbidden_decode)
    response = xor_client.post(
        "/api/v1/extractions",
        headers=bearer_auth_headers(),
        json={
            "source_ref": "doc://x",
            "document_base64": "A" * (DOCUMENT_BASE64_MAX_LENGTH + 1),
        },
    )
    assert response.status_code == 422
    assert decode_calls == []
