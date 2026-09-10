import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidIdpConnector
from app.domain.idp_connector import (
    require_connector_code,
    require_idp_source_ref,
    require_provider_code,
    require_public_domain,
)


def test_connector_code_accepts_snake_auth0_mark() -> None:
    assert require_connector_code("auth0_eu_desk") == "auth0_eu_desk"


def test_connector_code_rejects_uppercase_and_int() -> None:
    with pytest.raises(InvalidIdpConnector, match="oznaczenie"):
        require_connector_code("A")
    with pytest.raises(InvalidIdpConnector, match="oznaczenie"):
        require_connector_code(12)


@given(st.sampled_from(["auth0", "AUTH0", " Auth0 "]))
def test_provider_code_allowlist_auth0_only(raw: str) -> None:
    assert require_provider_code(raw) == "auth0"


@given(st.sampled_from(["", "okta", "azure", "google", "cognito", "hello"]))
def test_provider_code_rejects_other_idps(raw: str) -> None:
    with pytest.raises(InvalidIdpConnector, match="dostawca"):
        require_provider_code(raw)


def test_idp_source_ref_accepts_manual_and_auth0_fixture() -> None:
    assert require_idp_source_ref("tenant:manual") == "tenant:manual"
    assert require_idp_source_ref(" fixture://auth0/eu-1 ") == "fixture://auth0/eu-1"


@given(st.sampled_from(["", "   ", "https://auth0.com/x", "fixture://okta/1", "fixture://optima/1"]))
def test_idp_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidIdpConnector, match="obce"):
        require_idp_source_ref(raw)


def test_public_domain_blank_is_absent() -> None:
    assert require_public_domain(None) is None
    assert require_public_domain("") is None
    assert require_public_domain("  ") is None


def test_public_domain_accepts_hostname_text() -> None:
    assert require_public_domain(" Acme.eu.auth0.com ") == "acme.eu.auth0.com"


@given(
    st.sampled_from(
        [
            "https://acme.eu.auth0.com",
            "http://login.example",
            "acme.eu.auth0.com/jwks",
            "not a host",
            "auth0",
        ]
    )
)
def test_public_domain_rejects_issuer_url_and_bare_label(raw: str) -> None:
    with pytest.raises(InvalidIdpConnector, match="domena"):
        require_public_domain(raw)
