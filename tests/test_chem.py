from science_ops.tools.chem import calculate_dilution_final_volume, calculate_molarity


def test_molarity_basic():
    assert calculate_molarity(0.5, 1.0) == 0.5


def test_dilution_volume():
    assert calculate_dilution_final_volume(2.0, 10.0, 0.5) == 40.0
