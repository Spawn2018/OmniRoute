import pytest

from app.domain.errors import InvalidTrackingConsent
from app.domain.tracking_consent import parse_tracking_consent_row


def test_parse_tracking_consent_row_accepts_manual() -> None:
    code, kind, origin = parse_tracking_consent_row(
        "cns_party_01",
        "Party",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("cns_party_01", "party", "tenant:manual")


def test_parse_tracking_consent_row_rejects_poll_kind() -> None:
    with pytest.raises(InvalidTrackingConsent, match="rodzaj"):
        parse_tracking_consent_row("cns_party_01", "poll", "tenant:manual")
