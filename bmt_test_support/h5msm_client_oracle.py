"""Frozen provider observation oracle, reused for exact packet comparison only.

This never restores an object and is not an independent scientific calculation.
Only _hdf_snapshot's local test import is removed; functions share this module.
"""

import molsysmt as msm
import numpy as np
import pandas as pd
import pyunitwizard as puw


def _plain(value):
    """Observe public data independently; this oracle never restores a system."""
    if value is None or isinstance(value, (str, bool, int, float)):
        return value
    if value is pd.NA:
        return {'missing': True}
    if isinstance(value, np.generic):
        return {'scalar_dtype': str(value.dtype), 'value': _plain(value.item())}
    if isinstance(value, np.ndarray):
        return {
            'dtype': str(value.dtype),
            'shape': list(value.shape),
            'values': _plain(value.tolist()),
        }
    if isinstance(value, pd.DataFrame):
        return {
            'table': _plain(value.to_dict(orient='split')),
            'dtypes': list(map(str, value.dtypes)),
        }
    if isinstance(value, dict):
        return {key: _plain(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return {'sequence': type(value).__name__, 'values': [_plain(x) for x in value]}
    if puw.is_quantity(value):
        return {
            'unit': str(puw.get_unit(value)),
            'magnitude': _plain(puw.get_value(value)),
        }
    raise TypeError(f'Unobserved checkpoint field type: {type(value).__name__}')


def _snapshot(source):
    return _plain(
        {
            'topology': msm.convert(
                source.topology, to_form='molsysmt.TopologyDict'
            ).data,
            'chemical_states': msm.convert(
                source.chemical_states, to_form='molsysmt.ChemicalStatesDict'
            ).data,
            'structures': msm.convert(
                source.structures, to_form='molsysmt.StructuresDict'
            ),
            'state_associations': source.get(structure_chemical_state_index=True),
            'mechanics': source.molecular_mechanics.to_dict(),
            'mechanical_columns': source.molecular_mechanics.atoms_ff,
            'charge_assignment': source.molecular_mechanics.partial_charge_assignment,
            'type_assignment': source.molecular_mechanics.atom_type_assignment,
            'history': source.chemical_states.get_preparation_history(),
            'interactions': {
                name: result.to_dict() for name, result in source.interactions.items()
            },
        }
    )


def _hdf_snapshot(source):
    """Observe values under the two documented HDF transport normalizations.

    Structural schema 1 restores textual labels as object arrays. QuantityRecord
    restores scalar quantities as zero-dimensional arrays while retaining their
    numeric dtype and unit. Everything else keeps the strict checkpoint oracle.
    """
    result = _snapshot(source)
    labels = result['structures']['structure_id']
    if labels is not None and all(
        (isinstance(value, str) for value in labels['values'])
    ):
        labels['dtype'] = 'object'
    for name in (
        'cutoff_distance',
        'switch_distance',
        'hydrogen_mass',
        'salt_concentration',
        'kappa',
    ):
        value = result['mechanics'][name]
        if value is not None and (not isinstance(value['magnitude'], dict)):
            magnitude = np.asarray(value['magnitude'])
            value['magnitude'] = {
                'dtype': str(magnitude.dtype),
                'shape': [],
                'values': magnitude.item(),
            }
    return result
