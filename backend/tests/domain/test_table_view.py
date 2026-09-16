import pytest

from app.domain.errors import InvalidTableView
from app.domain.table_view import (
    default_mail_group_by,
    normalize_table_view_config,
    require_mail_group_by,
)


def test_default_group_by_is_party() -> None:
    assert default_mail_group_by() == "party"
    assert require_mail_group_by(None) == "party"
    assert require_mail_group_by("  ") == "party"
    assert require_mail_group_by("country") == "country"
    assert require_mail_group_by("status") == "status"


def test_thread_group_by_is_allowed() -> None:
    assert require_mail_group_by("thread") == "thread"
    assert normalize_table_view_config({"density": "compact", "group_by": "thread"})[
        "group_by"
    ] == "thread"


def test_normalize_config_rejects_chat() -> None:
    with pytest.raises(InvalidTableView, match="allowlist"):
        require_mail_group_by("chat")
    assert normalize_table_view_config({"density": "compact"}) == {"density": "compact"}
