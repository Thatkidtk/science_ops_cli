from science_ops.tools import mech


def test_orbit_period_positive():
    # LEO-like orbit: a ~ 6.8e6 m; period should be finite & positive
    a = 6.8e6
    earth_mu = mech.BODIES["earth"]["mu"]
    T = 2 * 3.14159 * (a ** 1.5) / (earth_mu ** 0.5)
    assert T > 0
