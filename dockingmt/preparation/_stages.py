"""Explicit provider orchestration behind the existing ligand preparation API."""

import molsysmt as msm

from dockingmt._private.smonitor import ArgumentError
from dockingmt.preparation._molsys import detached_provider_report


def stage_options(hydrogen_options, charge_options, typing_options=None):
    """Require explicit scientific choices before any molecular conversion."""
    for name, options in (
        ('hydrogen_options', hydrogen_options),
        ('charge_options', charge_options),
        ('typing_options', typing_options),
    ):
        if options is not None and (
            any(not isinstance(key, str) for key in options)
            or {'molecular_system', 'return_report', 'skip_digestion'} & options.keys()
        ):
            raise ArgumentError(
                arg_name=name,
                reason='Do not override the molecular input, report capture or argument digestion.',
            )
    if hydrogen_options is not None:
        if (
            hydrogen_options.get('mode') != 'fixed_chemical_state'
            or 'pH' not in hydrogen_options
            or hydrogen_options['pH'] is not None
            or not isinstance(hydrogen_options.get('engine'), str)
            or not hydrogen_options['engine'].strip()
        ):
            raise ArgumentError(
                arg_name='hydrogen_options',
                reason="Specify mode='fixed_chemical_state', pH=None and an explicit engine.",
            )
        hydrogen_options = dict(hydrogen_options)
        hydrogen_options.setdefault('attribute_policy', 'strict')
    if charge_options is not None:
        if (
            not isinstance(charge_options.get('method'), str)
            or not charge_options['method'].strip()
        ):
            raise ArgumentError(
                arg_name='charge_options',
                reason='Specify an explicit named MolSysMT charge method.',
            )
        charge_options = dict(charge_options)
    if typing_options is not None:
        if typing_options.get('typing_scheme') != 'autodock4' or (
            not isinstance(typing_options.get('method'), str)
            or not typing_options['method'].strip()
        ):
            raise ArgumentError(
                arg_name='typing_options',
                reason="Specify typing_scheme='autodock4' and an explicit named MolSysMT typing method.",
            )
        typing_options = dict(typing_options)
    return hydrogen_options, charge_options, typing_options


def run_stages(source, hydrogen_options, charge_options, typing_options=None):
    """Delegate stages without catching provider errors or choosing a fallback."""
    if hydrogen_options is None and charge_options is None and typing_options is None:
        return source, None
    input_n_atoms = int(msm.get(source, n_atoms=True))
    report = None
    if hydrogen_options is not None:
        result = msm.build.add_missing_hydrogens(
            source, return_report=True, **hydrogen_options
        )
        source = result['molecular_system']
        report = detached_provider_report(result['report'])
    if charge_options is not None:
        source = msm.build.assign_partial_charges(source, **charge_options)
    if typing_options is not None:
        source = msm.build.assign_autodock_atom_types(source, **typing_options)
    return source, {
        'schema_version': '1.0',
        'scope': 'explicit_molsysmt_stages',
        'input_n_atoms': input_n_atoms,
        'stages': (['hydrogen_addition'] if hydrogen_options is not None else [])
        + (['partial_charge_assignment'] if charge_options is not None else [])
        + (['atom_type_assignment'] if typing_options is not None else []),
        'hydrogen_addition': report,
        'charge_assignment_record': 'metadata.partial_charge_assignment'
        if charge_options is not None
        else None,
        **(
            {'type_assignment_record': 'metadata.atom_type_assignment'}
            if typing_options is not None
            else {}
        ),
    }


def finish_stage_maps(workflow, retained, written_order):
    """Compose index correspondence, including explicit absence for generated H."""
    if workflow is None:
        return None
    hydrogen_report = workflow['hydrogen_addition']
    correspondence = (
        hydrogen_report['atom_correspondence']
        if hydrogen_report is not None
        else [[i, i] for i in range(workflow['input_n_atoms'])]
    )
    output_to_input = {int(output): int(source) for source, output in correspondence}
    prepared_to_input = [output_to_input.get(int(i)) for i in retained]
    return {
        **workflow,
        'prepared_to_input_atom_indices': prepared_to_input,
        'pdbqt_to_input_atom_indices': [prepared_to_input[i] for i in written_order],
        'index_scope': 'selected_input_before_requested_stages',
        'generated_atom_marker': None,
    }
