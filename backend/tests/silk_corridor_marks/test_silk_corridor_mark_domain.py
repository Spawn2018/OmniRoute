import pytest

from app.domain.errors import InvalidSilkCorridorMark
from app.domain.silk_corridor_mark import parse_silk_corridor_mark_row


def test_parse_silk_corridor_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_silk_corridor_mark_row(
        "scm_block_01",
        "Block_Train",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("scm_block_01", "block_train", "tenant:manual")


def test_parse_silk_corridor_mark_row_rejects_unlocode_kind() -> None:
    with pytest.raises(InvalidSilkCorridorMark, match="rodzaj"):
        parse_silk_corridor_mark_row("scm_block_01", "cn_eu_pair", "tenant:manual")
