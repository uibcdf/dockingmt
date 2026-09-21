import numpy as np
import pytest
import pyunitwizard as puw

from dockingmt import BoxRegion, SearchDomain
from dockingmt._private.smonitor import ArgumentError


def test_box_region_creation_and_properties():
    center = puw.quantity([1.0, 2.0, 3.0], 'nm')
    lengths = puw.quantity([2.0, 2.0, 2.0], 'nm')

    box = BoxRegion(center=center, lengths=lengths, name='binding_site')

    assert isinstance(box, SearchDomain)
    assert box.name == 'binding_site'

    c_vals = puw.get_value(box.center)
    np.testing.assert_allclose(c_vals, [1.0, 2.0, 3.0])

    l_vals = puw.get_value(box.lengths)
    np.testing.assert_allclose(l_vals, [2.0, 2.0, 2.0])

    # Bounds: center +/- lengths/2 -> min [0, 1, 2], max [2, 3, 4]
    min_c, max_c = box.bounds
    np.testing.assert_allclose(puw.get_value(min_c), [0.0, 1.0, 2.0])
    np.testing.assert_allclose(puw.get_value(max_c), [2.0, 3.0, 4.0])

    # Volume: 2 * 2 * 2 = 8 nm^3
    v_val = puw.get_value(box.volume)
    assert pytest.approx(v_val) == 8.0


def test_box_region_unit_conversions():
    # Define in angstroms
    center = puw.quantity([10.0, 20.0, 30.0], 'angstrom')
    lengths = puw.quantity([15.0, 15.0, 15.0], 'angstrom')

    box = BoxRegion(center=center, lengths=lengths)

    # Stored internally in nm
    np.testing.assert_allclose(puw.get_value(box.center), [1.0, 2.0, 3.0])
    np.testing.assert_allclose(puw.get_value(box.lengths), [1.5, 1.5, 1.5])

    # Export to backend format in angstroms (AutoDock Vina convention)
    backend_box = box.to_backend_box(unit='angstrom')
    assert backend_box['unit'] == 'angstrom'
    np.testing.assert_allclose(backend_box['center'], (10.0, 20.0, 30.0))
    np.testing.assert_allclose(backend_box['lengths'], (15.0, 15.0, 15.0))


def test_box_region_dimensional_validation():
    # Dimensionless center
    with pytest.raises(ArgumentError, match="'center' must be a physical quantity"):
        BoxRegion(center=[1.0, 2.0, 3.0], lengths=puw.quantity([1.0, 1.0, 1.0], 'nm'))

    # Incompatible unit (time)
    with pytest.raises(ArgumentError, match='not compatible with length'):
        BoxRegion(
            center=puw.quantity([1.0, 2.0, 3.0], 'ps'),
            lengths=puw.quantity([1.0, 1.0, 1.0], 'nm'),
        )

    # Non-positive lengths
    with pytest.raises(ArgumentError, match='strictly positive'):
        BoxRegion(
            center=puw.quantity([1.0, 2.0, 3.0], 'nm'),
            lengths=puw.quantity([1.0, 0.0, 1.0], 'nm'),
        )


def test_box_region_contains():
    center = puw.quantity([0.0, 0.0, 0.0], 'nm')
    lengths = puw.quantity([2.0, 2.0, 2.0], 'nm')
    box = BoxRegion(center=center, lengths=lengths)

    inside_pt = puw.quantity([0.5, -0.5, 0.9], 'nm')
    assert box.contains(inside_pt) is True

    outside_pt = puw.quantity([1.5, 0.0, 0.0], 'nm')
    assert box.contains(outside_pt) is False

    # Inside when specified in angstroms
    inside_angstrom = puw.quantity([5.0, -5.0, 9.0], 'angstrom')
    assert box.contains(inside_angstrom) is True


def test_box_region_from_bounds():
    min_c = puw.quantity([1.0, 2.0, 3.0], 'nm')
    max_c = puw.quantity([3.0, 4.0, 5.0], 'nm')

    box = BoxRegion.from_bounds(min_coords=min_c, max_coords=max_c)
    np.testing.assert_allclose(puw.get_value(box.center), [2.0, 3.0, 4.0])
    np.testing.assert_allclose(puw.get_value(box.lengths), [2.0, 2.0, 2.0])

    # With padding
    pad = puw.quantity(0.5, 'nm')
    box_padded = BoxRegion.from_bounds(min_coords=min_c, max_coords=max_c, padding=pad)
    # Lengths should be 2.0 + 2*0.5 = 3.0
    np.testing.assert_allclose(puw.get_value(box_padded.lengths), [3.0, 3.0, 3.0])


def test_box_region_from_points():
    pts_raw = np.array(
        [
            [1.0, 1.0, 1.0],
            [3.0, 1.0, 1.0],
            [1.0, 5.0, 1.0],
            [1.0, 1.0, 7.0],
        ]
    )
    pts = puw.quantity(pts_raw, 'nm')

    box = BoxRegion.from_points(pts)
    # min: [1, 1, 1], max: [3, 5, 7] -> center: [2, 3, 4], lengths: [2, 4, 6]
    np.testing.assert_allclose(puw.get_value(box.center), [2.0, 3.0, 4.0])
    np.testing.assert_allclose(puw.get_value(box.lengths), [2.0, 4.0, 6.0])


def test_box_region_serialization_roundtrip():
    box = BoxRegion(
        center=puw.quantity([1.0, 2.0, 3.0], 'nm'),
        lengths=puw.quantity([1.5, 2.5, 3.5], 'nm'),
        name='catalytic_site',
    )
    serialized = box.to_dict()
    assert serialized['schema_version'] == '1.0'
    assert serialized['type'] == 'BoxRegion'
    assert serialized['name'] == 'catalytic_site'

    recovered = BoxRegion.from_dict(serialized)
    assert recovered.name == box.name
    np.testing.assert_allclose(
        puw.get_value(recovered.center), puw.get_value(box.center)
    )
    np.testing.assert_allclose(
        puw.get_value(recovered.lengths), puw.get_value(box.lengths)
    )


def test_box_region_from_molsysmt_selection():
    import molsysmt as msm

    path = msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm']
    pad = puw.quantity(0.2, 'nm')

    box = BoxRegion.from_selection(
        path,
        selection='atom_type != "H"',
        padding=pad,
        name='heavy_atoms_box',
    )

    assert box.name == 'heavy_atoms_box'
    assert box.center is not None
    assert box.lengths is not None
    # All lengths should be positive and greater than 2 * padding
    l_vals = puw.get_value(box.lengths)
    assert np.all(l_vals > 0.4)
    # Check Vina backend export
    vina_box = box.to_backend_box(unit='angstrom')
    assert vina_box['unit'] == 'angstrom'
    assert len(vina_box['center']) == 3
    assert len(vina_box['lengths']) == 3
