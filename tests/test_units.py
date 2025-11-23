from science_ops.tools.units import DIMENSIONS


def test_units_length_contains_meters():
    assert "m" in DIMENSIONS["length"]
