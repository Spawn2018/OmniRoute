from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.deps import require_tenant_session, set_authz_checker
from app.domain.tenant_contract_kek import (
    require_kek_code,
    require_kek_source_ref,
    require_wrap_kind,
)
from app.main import app
from app.models.tenant_contract_kek import TenantContractKek
from tests.http_auth import bearer_auth_headers

_KEY_LEAKS = (
    "password",
    "ciphertext",
    "key",
    "wrapped_dek",
    "unwrap",
    "secret",
    "plaintext",
    "buy_amount",
    "margin",
)


class PermitKekAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return True


class InMemoryKekMarkDesk:
    def __init__(self, session: object) -> None:
        self._session = session
        self.marks: list[TenantContractKek] = []

    async def list_marks(self) -> list[TenantContractKek]:
        return list(self.marks)

    async def persist_kek_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        kek_code: object,
        wrap_kind: object,
        source_ref: object,
    ) -> TenantContractKek:
        mark = TenantContractKek(
            id=uuid4(),
            organization_id=organization_id,
            kek_code=require_kek_code(kek_code),
            wrap_kind=require_wrap_kind(wrap_kind),
            source_ref=require_kek_source_ref(source_ref),
            created_by=user_id,
        )
        self.marks.append(mark)
        return mark


@pytest.fixture
def kek_http(monkeypatch: pytest.MonkeyPatch) -> object:
    desk = InMemoryKekMarkDesk(object())

    async def _session() -> object:
        handle = AsyncMock()
        handle.commit = AsyncMock()
        return handle

    monkeypatch.setattr(
        "app.api.tenant_contract_keks.TenantContractKekService",
        lambda _s: desk,
    )
    set_authz_checker(PermitKekAuthz())
    app.dependency_overrides[require_tenant_session] = _session
    yield TestClient(app), desk
    app.dependency_overrides.clear()
    set_authz_checker(None)


def _body(**extra: object) -> dict[str, object]:
    packed: dict[str, object] = {
        "kek_code": "desk_wrap_pl",
        "wrap_kind": "password",
        "source_ref": "fixture://kek/pl-1",
    }
    packed.update(extra)
    return packed


def _assert_no_key_material(payload: dict[str, object]) -> None:
    for leak in _KEY_LEAKS:
        assert leak not in payload


def test_http_create_and_list_kek_mark(kek_http: object) -> None:
    client, _desk = kek_http
    org_id = uuid4()
    headers = bearer_auth_headers(organization_id=org_id)
    created = client.post("/api/v1/tenant-contract-keks", headers=headers, json=_body())
    assert created.status_code == 201
    payload = created.json()
    assert payload["organization_id"] == str(org_id)
    assert payload["kek_code"] == "desk_wrap_pl"
    assert payload["wrap_kind"] == "password"
    _assert_no_key_material(payload)
    listed = client.get("/api/v1/tenant-contract-keks", headers=headers)
    assert listed.status_code == 200
    first = listed.json()[0]
    assert first["id"] == payload["id"]
    _assert_no_key_material(first)


def test_http_create_kms_wrap_kind_is_data(kek_http: object) -> None:
    client, _desk = kek_http
    created = client.post(
        "/api/v1/tenant-contract-keks",
        headers=bearer_auth_headers(),
        json=_body(wrap_kind="kms", source_ref="tenant:manual"),
    )
    assert created.status_code == 201
    assert created.json()["wrap_kind"] == "kms"
    _assert_no_key_material(created.json())


def test_http_create_bad_kek_code_is_400(kek_http: object) -> None:
    client, _desk = kek_http
    response = client.post(
        "/api/v1/tenant-contract-keks",
        headers=bearer_auth_headers(),
        json=_body(kek_code="X"),
    )
    assert response.status_code == 400
    assert "oznaczenie" in response.json()["detail"]


def test_http_create_unknown_wrap_kind_is_400(kek_http: object) -> None:
    client, _desk = kek_http
    response = client.post(
        "/api/v1/tenant-contract-keks",
        headers=bearer_auth_headers(),
        json=_body(wrap_kind="fernet"),
    )
    assert response.status_code == 400
    assert "owijka" in response.json()["detail"]


def test_http_create_foreign_source_ref_is_400(kek_http: object) -> None:
    client, _desk = kek_http
    response = client.post(
        "/api/v1/tenant-contract-keks",
        headers=bearer_auth_headers(),
        json=_body(source_ref="https://kms.example/x"),
    )
    assert response.status_code == 400
    assert "obce" in response.json()["detail"]


@pytest.mark.parametrize("secret_field", ["password", "ciphertext", "key"])
def test_http_create_rejects_secret_extra_fields(kek_http: object, secret_field: str) -> None:
    client, _desk = kek_http
    response = client.post(
        "/api/v1/tenant-contract-keks",
        headers=bearer_auth_headers(),
        json=_body(**{secret_field: "x"}),
    )
    assert response.status_code == 422
