from science_ops.tools.constants import CONSTANTS


def test_constants_has_speed_of_light():
    assert "c" in CONSTANTS
    assert CONSTANTS["c"]["unit"] == "m/s"
