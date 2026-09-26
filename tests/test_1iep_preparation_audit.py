import pytest

from devtools.audit_1iep_preparation import _compare_pdbqt, _pdbqt_inventory


def _atom(serial, x, charge, atom_type):
    return (
        f'ATOM  {serial:5d}  C   LIG A   1    '
        f'{x:8.3f}{0.0:8.3f}{0.0:8.3f}  1.00  0.00    '
        f'{charge:6.3f} {atom_type:<2}\n'
    ).encode()


def test_comparison_aligns_by_coordinate_instead_of_record_order():
    native = _atom(1, 1.0, 0.0, 'N') + _atom(2, 2.0, 0.0, 'C') + b'TORSDOF 0\n'
    reference = (
        _atom(2, 2.0, -0.2, 'C') + _atom(1, 1.0, 0.3, 'NA') + b'BRANCH 1 2\nTORSDOF 1\n'
    )

    result = _compare_pdbqt(native, reference)

    assert result['coordinate_matched_atoms'] == 2
    assert result['native_only_atoms'] == result['reference_only_atoms'] == 0
    assert result['matched_atom_type_disagreements'] == 1
    assert result['atom_type_disagreement_counts'] == [
        {'native': 'N', 'reference': 'NA', 'count': 1}
    ]
    assert result['matched_charge_mean_absolute_difference_e'] == pytest.approx(0.25)
    assert result['native_torsion_dof'] == 0
    assert result['reference_torsion_dof'] == 1
    assert result['reference_branch_count'] == 1


def test_duplicate_coordinates_are_rejected_as_ambiguous():
    with pytest.raises(ValueError, match='duplicate atom coordinates'):
        _pdbqt_inventory(_atom(1, 1.0, 0.0, 'C') + _atom(2, 1.0, 0.0, 'N'))
