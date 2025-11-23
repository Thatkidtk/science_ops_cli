from datetime import datetime, timezone

from science_ops.tools.astro import _parse_dec, _parse_ra, local_sidereal_time


def test_parse_ra_hours_to_degrees():
    assert abs(_parse_ra("10h") - 150.0) < 1e-6


def test_parse_dec_to_degrees():
    assert abs(_parse_dec("-12d30m") + 12.5) < 1e-6


def test_lst_in_range():
    dt = datetime(2024, 1, 1, tzinfo=timezone.utc)
    lst_deg = local_sidereal_time(dt, lon_deg=0.0)
    assert 0.0 <= lst_deg < 360.0
