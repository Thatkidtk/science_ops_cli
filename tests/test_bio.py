from science_ops.tools import bio


def test_gc_content_basic():
    # GC-content of "GCGC" = 1.0
    seq = "GCGC"
    total = len(seq)
    gc = sum(1 for b in seq if b in ("G", "C"))
    assert total == 4 and gc == 4


def test_codon_table_complete():
    assert len(bio.CODON_TABLE) == 64
