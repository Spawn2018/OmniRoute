import pytest

from app.domain.crm_dedup_mark import parse_crm_dedup_mark_row
from app.domain.errors import InvalidCrmDedupMark


def test_parse_crm_dedup_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_crm_dedup_mark_row(
        "crm_dedup_nip_01",
        "Nip",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("crm_dedup_nip_01", "nip", "tenant:manual")


def test_parse_crm_dedup_mark_row_rejects_merge_kind() -> None:
    with pytest.raises(InvalidCrmDedupMark, match="rodzaj"):
        parse_crm_dedup_mark_row("crm_dedup_nip_01", "merge", "tenant:manual")
