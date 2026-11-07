"""Compare fixed-score observations against their actual prepared inputs."""

import base64
import hashlib
import json
import os
from collections.abc import Mapping, Set
from pathlib import Path

import numpy as np
import pyunitwizard as puw
import smonitor
from argdigest import arg_digest

from dockingmt._private.smonitor import ArgumentError
from dockingmt._version import __version__
from dockingmt.core.pose_audit import audit_pose
from dockingmt.core.results import _molecular_atom_keys
from dockingmt.evaluation import _digest, _json_copy
from dockingmt.preparation import (
    PreparedLigand,
    PreparedReceptor,
    audit_preparation_charges,
)
from dockingmt.preparation._export import export_pdbqt
from dockingmt.preparation._molsys import (
    detached_provider_report,
    source_atom_types,
    source_charge_assignment,
)


def _require(condition, reason, position=None):
    if not condition:
        prefix = f'Pose at position {position}: ' if position is not None else ''
        raise ArgumentError(arg_name='comparison', reason=prefix + reason)


def _same(left, right):
    """Compare JSON declarations without equating booleans and numbers."""
    return json.dumps(left, sort_keys=True, allow_nan=False) == json.dumps(
        right, sort_keys=True, allow_nan=False
    )


def _evaluation(pose, score_name, position):
    record = pose.to_dict()
    history = record['metadata'].get('scoring_history', [])
    _require(isinstance(history, list), 'Supply a scoring history.', position)
    entries = [
        entry
        for entry in history
        if isinstance(entry, Mapping)
        and isinstance(entry.get('scores'), Mapping)
        and score_name in entry['scores']
    ]
    _require(
        len(entries) == 1,
        'The selected score needs exactly one recorded scoring evaluation.',
        position,
    )
    entry = entries[0]
    _require(
        isinstance(entry.get('score_definitions'), Mapping),
        'Supply descriptors for the selected evaluation.',
        position,
    )
    definition = pose.score_definitions.get(score_name, {})
    _require(
        definition.get('component') == 'lig_inter'
        and definition.get('method') in ('AutoDock Vina/vina', 'AutoDock Vina/vinardo')
        and definition.get('method_version') == '1.2.7',
        'This profile supports fixed Vina/Vinardo 1.2.7 lig_inter only.',
        position,
    )
    _require(
        definition.get('unit') == str(puw.get_unit(puw.quantity(1, 'kcal/mol'))),
        'This profile consumes reported kcal/mol values without rescaling.',
        position,
    )
    for name, value in entry.get('scores', {}).items():
        _require(
            name in record['scores']
            and _same(value, record['scores'][name])
            and _same(
                entry.get('score_definitions', {}).get(name),
                pose.score_definitions.get(name),
            ),
            'The evaluation disagrees with current scores or descriptors.',
            position,
        )
    # Inspect this producer independently; collection-owned old docking scores
    # remain with the original collection, rather than being assigned to it.
    selected = {
        **record,
        'scores': entry.get('scores', {}),
        'metadata': {
            **record['metadata'],
            'score_definitions': entry.get('score_definitions', {}),
            'scoring_history': [entry],
        },
    }
    audit = audit_pose(selected)
    _require(
        audit['status'] == 'consistent',
        'The selected evaluation needs complete, consistent input captures and reference evidence.',
        position,
    )
    context = definition['context']
    _require(
        set(context)
        == {
            'reference_energy_policy',
            'stage',
            'receptor_sha256',
            'partner_sha256',
            'backend_box',
            'weights',
            'grid_spacing',
            'preparation_assessment',
        },
        'Unsupported or missing comparison-context fields.',
        position,
    )
    _require(context['stage'] == 'scoring', 'Use fixed scoring observations.', position)
    return record, entry, definition, audit


def _receptor_bytes(receptor):
    if isinstance(receptor, PreparedReceptor):
        return receptor.to_pdbqt().encode()
    if isinstance(receptor, str) and receptor.startswith('pdbqt_text:'):
        return receptor.removeprefix('pdbqt_text:').encode()
    if isinstance(receptor, (str, Path)) and os.path.isfile(receptor):
        return Path(receptor).read_bytes()
    if isinstance(receptor, str) and ('ATOM' in receptor or 'HETATM' in receptor):
        return receptor.encode()
    _require(
        isinstance(receptor, (str, Path)),
        'Supply a prepared receptor or a PDBQT input.',
    )
    return Path(receptor).read_bytes()


def _assignment_policy(report):
    _require(isinstance(report, dict), 'Named preparation attribution is required.')
    return {
        key: report[key]
        for key in (
            'schema',
            'method',
            'engine',
            'software',
            'parameters',
            'typing_scheme',
            'rule_version',
            'hydrogen_policy',
        )
        if key in report
    }


def _prepared_view(problem, pose, entry, definition, position):
    import molsysmt as msm

    from dockingmt.core.problem import DockingProblem
    from dockingmt.engines._vina_scoring import _input_pose
    from dockingmt.engines.vina import _vina_box

    _require(
        isinstance(problem, DockingProblem),
        'Supply one matching DockingProblem per pose.',
        position,
    )
    prepared = problem.partner
    _require(
        isinstance(prepared, PreparedLigand) and prepared.source_molsys is not None,
        'Supply a PreparedLigand with its complete molecular source.',
        position,
    )
    _require(
        prepared.state_id == pose.partner_state_id,
        'The prepared ligand state disagrees with the pose.',
        position,
    )
    for role in ('partner', 'receptor'):
        declared = problem.metadata.get(f'{role}_state_id')
        _require(
            declared is None or declared == getattr(pose, f'{role}_state_id'),
            f'The problem {role} state disagrees with the pose.',
            position,
        )
    if isinstance(problem.receptor, PreparedReceptor):
        _require(
            problem.receptor.state_id == pose.receptor_state_id,
            'The prepared receptor state disagrees with the pose.',
            position,
        )
    context = definition['context']
    center, size = _vina_box(problem.search_domain)
    _require(
        _same(
            context['backend_box'], {'center': center, 'size': size, 'unit': 'angstrom'}
        ),
        'The problem domain differs from the recorded scoring box.',
        position,
    )
    _require(
        hashlib.sha256(_receptor_bytes(problem.receptor)).hexdigest()
        == context['receptor_sha256'],
        'The supplied receptor differs from the captured input.',
        position,
    )
    exported = export_pdbqt(prepared, ligand=True)
    _require(
        exported.atom_map.get('schema') == 'molsysmt.atom_export@1'
        and exported.atom_map.get('charge_unit') == 'elementary_charge',
        'Use the supported provider export map and canonical elementary-charge values.',
        position,
    )
    content = exported.text.encode()
    _require(
        hashlib.sha256(content).hexdigest()
        == context['partner_sha256']
        == exported.atom_map['payload_sha256'],
        'The prepared export differs from the captured ligand input.',
        position,
    )
    _require(
        content
        == base64.b64decode(
            entry['backend_artifacts']['partner']['content_base64'], validate=True
        ),
        'The prepared export differs from captured bytes.',
        position,
    )
    _, geometry = _input_pose(
        prepared,
        content,
        {'partner': pose.partner_state_id, 'receptor': pose.receptor_state_id},
        pose,
    )
    charges = audit_preparation_charges(prepared)
    _require(
        charges['assessment'] == 'consistent',
        'Supply consistent named charge evidence.',
        position,
    )
    # Use attribution on the actual exported view: edited fields can invalidate
    # it through MolSysMT even when the original prepared metadata still exists.
    # Public extraction validates the provider's actual numeric/chemical
    # binding and projects legitimate derived assignments. Retain both producers.
    native = exported.molecular_system
    original_assignments = {
        'charges': detached_provider_report(
            native.molecular_mechanics.partial_charge_assignment
        ),
        'typing': detached_provider_report(
            native.molecular_mechanics.atom_type_assignment
        ),
    }
    checked = msm.extract(native, selection=list(range(prepared.n_atoms)))
    assignment = source_charge_assignment(checked)
    _, typing = source_atom_types(checked, prepared.n_atoms)
    policy = {
        key: prepared.metadata.get(key)
        for key in ('hydrogen_policy', 'torsion_policy', 'active_torsion_bonds')
    }
    _require(
        all(value is not None for value in policy.values()),
        'Record H and torsion preparation policies.',
        position,
    )
    policy['charges'] = _assignment_policy(assignment)
    policy['typing'] = _assignment_policy(typing)
    _require(
        bool(policy['charges'].get('method')) and bool(policy['typing'].get('method')),
        'Record named charge and typing methods.',
        position,
    )
    evidence = {
        'prepared': detached_provider_report(prepared.to_dict()),
        'export': detached_provider_report(exported.atom_map),
        'geometry_check': geometry,
        'charge_audit': charges,
        'preparation_policy': policy,
        'validated_charge_assignment': assignment,
        'validated_type_assignment': typing,
        'original_exported_assignments': original_assignments,
    }
    return exported.molecular_system, evidence


def _correspondence(system, reference, keys, reference_keys, position):
    import molsysmt as msm

    _require(
        keys == reference_keys,
        'This profile requires the same ordered native atom identities; supply an admitted common axis.',
        position,
    )
    candidate = [[i, i] for i in range(len(keys))]
    report = msm.chemical_states.get_atom_correspondences(
        system,
        reference_molecular_system=reference,
        structure_indices=0,
        reference_structure_indices=0,
        chemical_state='structure',
        reference_chemical_state='structure',
        candidate_atom_correspondences=[candidate],
        max_matches=1,
    )
    report = detached_provider_report(report)
    _require(
        report.get('schema') == 'molsysmt.atom_correspondences@1'
        and report.get('method') == 'declared_graph_isomorphism'
        and report.get('rule_version') == 'declared_graph_isomorphism@1'
        and report.get('evidence', {}).get('kind') == 'declared_complete_covalent_graph'
        and report.get('search_scope') == 'supplied_atom_correspondences'
        and report.get('search_complete') is True
        and report.get('atom_correspondences') == [candidate],
        'MolSysMT did not admit complete chemical correspondence on the supplied axis.',
        position,
    )
    return _json_copy(report, 'correspondence')


@smonitor.signal(tags=['api', 'analysis', 'comparison'])
@arg_digest(config='dockingmt._argdigest')
def compare_scores(result, score_name, *, problems, ascending):
    """Compare fixed ``lig_inter`` observations using matching preparations.

    Supply one DockingProblem per result pose, in result order, with a complete
    PreparedLigand source. The bounded profile supports Vina/Vinardo 1.2.7,
    one method, matching states/context, the same ordered native atom identities,
    conserved charges/types/torsions and compatible named preparation policies.
    ``ascending`` explicitly chooses lower/higher reported values first.

    MolSysMT exports the actual prepared views and validates supplied chemical
    correspondences. This performs molecular IO/identity checks, but no search,
    scoring, H generation, charge assignment or typing calculation. It needs
    MolSysMT's declared-graph capability, not an installed Vina engine.

    Return an independent finite JSON report with tied groups, original ranks,
    exact input identities and evidence. Failure raises ArgumentError (provider
    errors propagate); no successful subset is returned. Source ranks/histories
    are preserved. Consistent supplied records are not authenticated producers,
    experimental validity, affinity or a common Vina/Vinardo scale.
    """
    _require(
        not isinstance(problems, Set),
        'Supply problems in result order, not an unordered set.',
    )
    problems = list(problems)
    _require(
        len(result) >= 2 and len(problems) == len(result),
        'Supply at least two poses and exactly one matching problem per pose.',
    )
    snapshot = result.to_dict()
    states = [(pose.partner_state_id, pose.receptor_state_id) for pose in result]
    _require(
        all(
            all(isinstance(state, str) and state.strip() for state in pair)
            for pair in states
        )
        and len(set(states)) == 1,
        'Declare the same nonempty partner/receptor state identifiers for every pose.',
    )
    ids = [pose.pose_id for pose in result]
    _require(
        all(isinstance(value, str) and value.strip() for value in ids)
        and len(set(ids)) == len(ids),
        'Supply unique nonempty pose identifiers.',
    )
    evaluations = [
        _evaluation(pose, score_name, position)
        for position, pose in enumerate(result, 1)
    ]
    reference_definition = None
    for position, (_, entry, definition, _) in enumerate(evaluations, 1):
        common_definition = {
            **definition,
            'evaluation_producer': {
                key: entry.get(key)
                for key in (
                    'backend',
                    'backend_version',
                    'dockingmt_version',
                    'molsysmt_version',
                    'applied_parameters',
                )
            },
            'context': {
                key: value
                for key, value in definition['context'].items()
                if key != 'partner_sha256'
            },
        }
        if reference_definition is not None:
            _require(
                _same(common_definition, reference_definition),
                'Method, version, units or shared comparison context differs.',
                position,
            )
        reference_definition = common_definition
    rows = []
    reference = reference_keys = reference_model = reference_charges = None
    for position, (pose, problem, evaluation) in enumerate(
        zip(result, problems, evaluations), 1
    ):
        record, entry, definition, audit = evaluation
        system, evidence = _prepared_view(problem, pose, entry, definition, position)
        keys = _molecular_atom_keys(system)
        if reference is None:
            reference, reference_keys = system, keys
        evidence['chemical_correspondence'] = _correspondence(
            system, reference, keys, reference_keys, position
        )
        export = evidence['export']
        model = {
            key: export.get(key)
            for key in (
                'output_to_source_atom_indices',
                'source_atom_ids',
                'source_atom_names',
                'source_atom_types',
                'output_atom_ff_types',
                'torsion_tree',
            )
        }
        model['policy'] = evidence['preparation_policy']
        charges = np.asarray(export['partial_charge_before_rounding'], dtype=float)
        if reference_model is not None:
            _require(
                _same(model, reference_model),
                'Prepared atom types, torsions, axes or preparation policy differs.',
                position,
            )
            _require(
                charges.shape == reference_charges.shape
                and np.allclose(charges, reference_charges, rtol=0, atol=1e-12),
                'Prepared charges differ beyond 1e-12 elementary charge.',
                position,
            )
        else:
            reference_model, reference_charges = model, charges
        rows.append(
            {
                'position': position,
                'pose_id': pose.pose_id,
                'original_rank': pose.rank,
                'partner_state_id': pose.partner_state_id,
                'receptor_state_id': pose.receptor_state_id,
                'value': pose.scores[score_name],
                'definition': definition,
                'source_pose_record_sha256': _digest(record),
                'evaluation_audit': audit,
                'reference_energy': entry['reference_energy'],
                'evaluation_producer': {
                    key: entry.get(key)
                    for key in (
                        'backend',
                        'backend_version',
                        'dockingmt_version',
                        'molsysmt_version',
                        'applied_parameters',
                    )
                },
                'scoring_evaluation_record_sha256': _digest(entry),
                'prepared_evidence': evidence,
            }
        )
    ordered = sorted(rows, key=lambda row: row['value'], reverse=not ascending)
    groups = []
    for row in ordered:
        if not groups or row['value'] != groups[-1]['value']:
            groups.append({'value': row['value'], 'positions': []})
        groups[-1]['positions'].append(row['position'])
    return _json_copy(
        {
            'schema_version': '1.0',
            'comparison_type': 'prepared_fixed_lig_inter',
            'profile': 'vina_1.2.7_same_axis@1',
            'score_name': score_name,
            'policy': {
                'ascending': ascending,
                'ties': 'equal_reported_values',
                'tie_presentation': 'source_order',
                'charge_tolerance': {'value': 1e-12, 'unit': 'elementary_charge'},
            },
            'source_result_record_sha256': _digest(snapshot),
            'rows': rows,
            'display_order': [row['position'] for row in ordered],
            'groups': groups,
            'producer': {'dockingmt_version': __version__},
            'scope': 'Comparison of supplied recorded observations and currently verified prepared views; producer authentication and experimental validity are not established.',
        },
        'comparison',
    )
