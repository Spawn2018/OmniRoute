import pytest

from app.domain.errors import InvalidTelematicsDevice
from app.domain.telematics_device import parse_telematics_device_row


def test_parse_telematics_device_row_accepts_manual() -> None:
    code, kind, origin = parse_telematics_device_row(
        "trk_yard_01",
        "Tracker",
        "tenant:manual",
    )
    assert (code, kind, origin) == ("trk_yard_01", "tracker", "tenant:manual")


def test_parse_telematics_device_row_rejects_poll_kind() -> None:
    with pytest.raises(InvalidTelematicsDevice, match="rodzaj"):
        parse_telematics_device_row("trk_yard_01", "poll", "tenant:manual")
