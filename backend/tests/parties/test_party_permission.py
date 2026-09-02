from pathlib import Path
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.api.deps import set_authz_checker
from app.integrations.openfga.model import authorization_model_request
from app.main import app
from tests.http_auth import bearer_auth_headers

_ROOT = Path(__file__).resolve().parents[3]
_DENIED = "Brak uprawnienia can_manage_parties na organization"
_ENDPOINTS = (
    ("GET", "/api/v1/parties", None, None),
    ("GET", "/api/v1/parties/resolve", {"tax_id": "5252345178"}, None),
    ("GET", "/api/v1/parties/resolve-email", {"email": "a@acme.test"}, None),
    ("POST", "/api/v1/parties/lookup", None, {"tax_id": "5252345178", "country_code": "PL"}),
    ("POST", "/api/v1/parties/iban-lookup", None, {"iban": "PL61109010140000071219812874"}),
    (
        "POST",
        "/api/v1/parties",
        None,
        {
            "legal_name": "ACME Sp. z o.o.",
            "country_code": "PL",
            "roles": ["customer"],
        },
    ),
    ("GET", "/api/v1/party-scorecards", None, None),
    (
        "GET",
        "/api/v1/party-scorecards/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        None,
        None,
    ),
    (
        "POST",
        "/api/v1/party-scorecards/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        None,
        {"sample_size": 0, "window_days": 90},
    ),
    ("GET", "/api/v1/customer-sops", None, None),
    (
        "GET",
        "/api/v1/customer-sops/resolve",
        {"party_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa", "code": "booking"},
        None,
    ),
    (
        "POST",
        "/api/v1/customer-sops",
        None,
        {
            "party_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "code": "booking",
            "title": "Booking",
            "body": "zarezerwuj slot",
        },
    ),
    (
        "POST",
        "/api/v1/customer-sops/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa/approve",
        None,
        None,
    ),
    ("GET", "/api/v1/credit-reviews", None, None),
    (
        "GET",
        "/api/v1/credit-reviews/resolve",
        {
            "party_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "on_date": "2026-09-01",
        },
        None,
    ),
    (
        "POST",
        "/api/v1/credit-reviews",
        None,
        {
            "party_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "review_date": "2026-09-01",
            "decision": "ok",
        },
    ),
)


class DenyAllAuthz:
    async def check(
        self,
        *,
        user_id: UUID,
        relation: str,
        object_type: str,
        object_id: UUID,
    ) -> bool:
        return False


@pytest.fixture(autouse=True)
def _reset_authz():
    set_authz_checker(None)
    yield
    set_authz_checker(None)


@pytest.mark.parametrize(("method", "path", "params", "json_body"), _ENDPOINTS)
def test_party_endpoints_are_forbidden_without_can_manage_parties(
    method: str,
    path: str,
    params: dict[str, str] | None,
    json_body: dict[str, object] | None,
) -> None:
    set_authz_checker(DenyAllAuthz())
    response = TestClient(app).request(
        method,
        path,
        headers=bearer_auth_headers(),
        params=params,
        json=json_body,
    )
    assert response.status_code == 403
    assert response.json()["detail"] == _DENIED


def test_authorization_model_grants_parties_to_organization_member() -> None:
    organization = next(
        definition
        for definition in authorization_model_request().type_definitions
        if definition.type == "organization"
    )
    relation = organization.relations["can_manage_parties"]
    assert relation.computed_userset is not None
    assert relation.computed_userset.relation == "member"


def test_fga_source_declares_parties_relation_without_changing_geography() -> None:
    source = (_ROOT / "authz" / "model.fga").read_text(encoding="utf-8")
    assert "can_manage_parties: member" in source
    assert "can_manage_geography: member" in source
    assert "can_manage_credit_reviews" not in source
