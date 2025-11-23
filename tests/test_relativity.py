from science_ops.tools import relativity


def test_gamma_beta_zero_is_one():
    gamma = relativity._gamma_from_beta(0.0)
    assert abs(gamma - 1.0) < 1e-12
