from datetime import time
from uuid import uuid4

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.errors import InvalidGroupageLine
from app.domain.groupage_line import (
    require_cutoff_local,
    require_distinct_line_ends,
    require_line_code,
    require_line_location_kind,
    require_line_source_ref,
    require_line_transit_days,
    require_operating_dows,
)


def test_groupage_line_allowlists() -> None:
    assert require_line_code(" WA-HUB ") == "wa_hub"
    assert require_cutoff_local("16:30") == time(16, 30)
    assert require_cutoff_local(time(7, 0, 0)) == time(7, 0, 0)
    assert require_line_transit_days(3) == 3
    assert require_operating_dows([5, 1, 1]) == [1, 5]
    assert require_line_location_kind("postal_zone") == "postal_zone"
    assert require_line_source_ref("fixture://groupage-line/a") == "fixture://groupage-line/a"


def test_groupage_line_rejects_port_zero_days_and_empty_dows() -> None:
    with pytest.raises(InvalidGroupageLine, match="UN/LOCODE"):
        require_line_location_kind("unlocode")
    with pytest.raises(InvalidGroupageLine, match="1 dzień"):
        require_line_transit_days(0)
    with pytest.raises(InvalidGroupageLine, match="puste"):
        require_operating_dows([])
    with pytest.raises(InvalidGroupageLine, match="float"):
        require_cutoff_local(16.5)
    with pytest.raises(InvalidGroupageLine, match="obce"):
        require_line_source_ref("https://evil.example/line")
    same = uuid4()
    with pytest.raises(InvalidGroupageLine, match="różne"):
        require_distinct_line_ends(same, same)


@given(st.sampled_from(["1line", "x", "line!"]))
def test_line_code_is_not_loose_label(raw: str) -> None:
    with pytest.raises(InvalidGroupageLine, match="snake"):
        require_line_code(raw)
