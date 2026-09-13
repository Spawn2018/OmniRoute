import pytest

from app.domain.errors import InvalidRoutePlanMark
from app.domain.route_plan_mark import parse_route_plan_mark_row


def test_parse_route_plan_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_route_plan_mark_row(
        "route_gdn_osl",
        "Route",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("route_gdn_osl", "route", "tenant:manual")


def test_parse_route_plan_mark_row_rejects_solver_kind() -> None:
    with pytest.raises(InvalidRoutePlanMark, match="rodzaj"):
        parse_route_plan_mark_row("route_gdn_osl", "valhalla", "tenant:manual")
