import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidInboundMessage, InvalidSourceRef
from app.domain.inbound_message import (
    inbound_draft_status,
    inbound_extract_text,
    require_body_text,
    require_external_id,
    require_from_address,
    require_graph_source_ref,
    require_inbound_source_ref,
    require_mailbox_source_ref,
    require_subject,
)


def test_inbound_draft_status_is_draft() -> None:
    assert inbound_draft_status() == "draft"


def test_require_inbound_source_ref_accepts_fixture() -> None:
    assert require_inbound_source_ref(" fixture://inbound-mail/1 ") == "fixture://inbound-mail/1"


def test_require_inbound_source_ref_accepts_synth() -> None:
    assert require_inbound_source_ref("synth://mail/demo") == "synth://mail/demo"


def test_require_graph_source_ref_accepts_graph() -> None:
    assert require_graph_source_ref(" graph://inbox/1 ") == "graph://inbox/1"


def test_require_graph_source_ref_rejects_fixture() -> None:
    with pytest.raises(InvalidInboundMessage, match="graph://"):
        require_graph_source_ref("fixture://inbound-mail/1")


def test_require_mailbox_source_ref_accepts_prefix() -> None:
    assert require_mailbox_source_ref(" imap://inbox/1 ") == "imap://inbox/1"


def test_require_mailbox_source_ref_rejects_graph() -> None:
    with pytest.raises(InvalidInboundMessage, match="imap"):
        require_mailbox_source_ref("graph://inbox/1")


def test_require_external_id_rejects_blank() -> None:
    with pytest.raises(InvalidInboundMessage, match="obowiązkowy"):
        require_external_id("  ")


def test_require_inbound_source_ref_rejects_imap() -> None:
    with pytest.raises(InvalidInboundMessage, match="fixture"):
        require_inbound_source_ref("imap://inbox")


def test_require_inbound_source_ref_rejects_blank() -> None:
    with pytest.raises(InvalidSourceRef, match="obowiązkowy"):
        require_inbound_source_ref("   ")


def test_require_from_address_lowers() -> None:
    assert require_from_address("  Ops@Example.COM ") == "ops@example.com"


def test_require_from_address_rejects_non_email() -> None:
    with pytest.raises(InvalidInboundMessage, match="e-mail"):
        require_from_address("not-an-address")


def test_require_from_address_rejects_non_text() -> None:
    with pytest.raises(InvalidInboundMessage, match="tekstem"):
        require_from_address(12)  # type: ignore[arg-type]


def test_require_subject_strips() -> None:
    assert require_subject("  RFQ Gdynia  ") == "RFQ Gdynia"


def test_require_subject_rejects_blank() -> None:
    with pytest.raises(InvalidInboundMessage, match="temat"):
        require_subject("  ")


def test_require_body_text_rejects_blank() -> None:
    with pytest.raises(InvalidInboundMessage, match="treść"):
        require_body_text("\n")


@given(local=st.from_regex(r"[a-z][a-z0-9]{0,11}", fullmatch=True))
def test_from_address_roundtrip_lower(local: str) -> None:
    raw = f"{local.upper()}@carrier.example"
    assert require_from_address(raw) == f"{local}@carrier.example"


def test_inbound_extract_text_joins_subject_and_body() -> None:
    assert inbound_extract_text("RFQ", "1x40HC") == "RFQ\n\n1x40HC"


def test_inbound_extract_text_rejects_over_extract_limit() -> None:
    with pytest.raises(InvalidInboundMessage, match="extract"):
        inbound_extract_text("RFQ", "x" * 50_000)
