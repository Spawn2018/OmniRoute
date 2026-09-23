from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.document_template import (
    require_branding_ref,
    require_layout_ref,
    require_output_kind,
    require_template_kind,
    require_template_language,
    require_template_source_ref,
)
from app.domain.errors import InvalidDocumentTemplate


@given(st.sampled_from(["own_label", "cmr"]))
def test_template_kind_allowlist(raw: str) -> None:
    assert require_template_kind(raw) == raw


@given(st.sampled_from(["network_label", "hbl", "quotation", "OWN_LABEL"]))
def test_template_kind_rejects_unknown(raw: str) -> None:
    with pytest.raises(InvalidDocumentTemplate, match="rodzaj"):
        require_template_kind(raw)


@given(st.from_regex(r"\A[a-z0-9][a-z0-9_-]{1,63}\Z"))
def test_layout_ref_accepts_snake(raw: str) -> None:
    assert require_layout_ref(raw) == raw


@given(st.sampled_from(["", "A", "Own Label", "x/y", "a" * 65]))
def test_layout_ref_rejects_empty_upper_slash_long(raw: str) -> None:
    with pytest.raises(InvalidDocumentTemplate, match="układ"):
        require_layout_ref(raw)


def test_branding_ref_none_and_blank() -> None:
    assert require_branding_ref(None) is None
    assert require_branding_ref("") is None
    assert require_branding_ref("  ") is None


@given(st.from_regex(r"\A[a-z0-9][a-z0-9_-]{1,63}\Z"))
def test_branding_ref_accepts_snake(raw: str) -> None:
    assert require_branding_ref(raw) == raw


@given(st.sampled_from(["A", "Own Brand", "x/y", "a" * 65]))
def test_branding_ref_rejects_bad_shape(raw: str) -> None:
    with pytest.raises(InvalidDocumentTemplate, match="branding"):
        require_branding_ref(raw)


@given(st.sampled_from(["pl", "en"]))
def test_template_language_allowlist(raw: str) -> None:
    assert require_template_language(raw) == raw


@given(st.sampled_from(["de", "PL", "pol"]))
def test_template_language_rejects_unknown(raw: str) -> None:
    with pytest.raises(InvalidDocumentTemplate, match="język"):
        require_template_language(raw)


@given(st.sampled_from(["html_print", "pdf", "zpl"]))
def test_output_kind_allowlist(raw: str) -> None:
    assert require_output_kind(raw) == raw


@given(st.sampled_from(["HTML_PRINT", "docx", "png", "zebra"]))
def test_output_kind_rejects_unknown(raw: str) -> None:
    with pytest.raises(InvalidDocumentTemplate, match="wyjście"):
        require_output_kind(raw)


def test_template_source_ref_accepts_fixture() -> None:
    assert (
        require_template_source_ref(" fixture://document-template/1 ")
        == "fixture://document-template/1"
    )


@given(st.sampled_from(["", "   ", "http://hold.example/x"]))
def test_template_source_ref_rejects_empty_and_foreign(raw: str) -> None:
    with pytest.raises(InvalidDocumentTemplate):
        require_template_source_ref(raw)


def test_template_kind_rejects_uuid_as_kind() -> None:
    with pytest.raises(InvalidDocumentTemplate, match="rodzaj"):
        require_template_kind(uuid4())  # type: ignore[arg-type]
