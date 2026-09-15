import pytest

from app.domain.errors import InvalidModelFeatureMark
from app.domain.model_feature_mark import parse_model_feature_mark_row


def test_parse_model_feature_mark_row_accepts_manual() -> None:
    code, kind, origin = parse_model_feature_mark_row(
        "mf_numeric_01",
        "Numeric",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("mf_numeric_01", "numeric", "tenant:manual")


def test_parse_model_feature_mark_row_rejects_live_kind() -> None:
    with pytest.raises(InvalidModelFeatureMark, match="rodzaj"):
        parse_model_feature_mark_row(
            "mf_numeric_01",
            "auto_train",
            "tenant:manual",
        )
