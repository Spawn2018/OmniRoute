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


def test_thread_group_by_is_rejected() -> None:
    with pytest.raises(InvalidTableView, match="allowlist"):
        require_mail_group_by("thread")


def test_normalize_config_rejects_thread() -> None:
    with pytest.raises(InvalidTableView, match="allowlist"):
        normalize_table_view_config({"density": "compact", "group_by": "thread"})


def test_normalize_config_keeps_other_keys_when_group_missing() -> None:
    assert normalize_table_view_config({"density": "compact"}) == {"density": "compact"}
