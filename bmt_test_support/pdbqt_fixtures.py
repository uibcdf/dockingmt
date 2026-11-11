"""Fixed PDBQT controls from tests/test_engines.py at producer9a40e38.

These original literal bytes are test inputs, not new molecular observations.
No scientific provider or optional engine is imported by this support module.
"""

MINIMAL_REC_PDBQT = """ATOM      1  N   ALA A   1       0.000   0.000   0.000  1.00  0.00     0.000 N
ATOM      2  CA  ALA A   1       1.458   0.000   0.000  1.00  0.00     0.000 C
ATOM      3  C   ALA A   1       2.009   1.428   0.000  1.00  0.00     0.000 C
ATOM      4  O   ALA A   1       1.246   2.392   0.000  1.00  0.00     0.000 OA
"""

MINIMAL_LIG_PDBQT = """ROOT
ATOM      1  C1  LIG A   1       0.000   0.000   0.000  1.00  0.00     0.000 C
ATOM      2  C2  LIG A   1       1.500   0.000   0.000  1.00  0.00     0.000 C
ENDROOT
TORSDOF 0
"""
