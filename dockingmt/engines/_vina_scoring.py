"""The bounded prepared-conformation consumer of Vina.score()."""

from copy import deepcopy

import molsysmt as msm
import numpy as np
import pyunitwizard as puw

from dockingmt._private.serialization import validate_schema_version
from dockingmt._private.smonitor import ArgumentError
from dockingmt._version import __version__
from dockingmt.core._scores import normalize_definitions
from dockingmt.core.problem import _is_pdbqt_input
from dockingmt.core.protocol import VinaProtocol, _validate_vina_intent
from dockingmt.core.results import DockingPose, _molecular_atom_keys, _normalize_scores
from dockingmt.engines.vina import _cleanup_staged_files, _vina_box, _VinaTimings
from dockingmt.preparation import PreparedLigand, PreparedReceptor, assess_preparation

# Half a PDBQT coordinate's three-decimal-Angstrom rendering step, plus
# numerical conversion noise. This does not match or infer molecular identity.
GEOMETRY_TOLERANCE_ANGSTROM = 0.000500001
COMPONENTS = (
    'total',
    'lig_inter',
    'flex_inter',
    'other_inter',
    'flex_intra',
    'lig_intra',
    'torsions',
    'lig_intra_best_pose',
)


def _history(pose):
    history = pose.metadata.get('scoring_history', [])
    if not isinstance(history, list):
        raise ArgumentError(
            arg_name='scoring_history', reason='Use a list of evaluations.'
        )
    for entry in history:
        validate_schema_version(entry, 'ScoringEvaluation')
        if entry.get('operation') != 'score':
            raise ArgumentError(
                arg_name='scoring_history', reason='Declare a score operation.'
            )
        normalize_definitions(
            entry.get('score_definitions'), _normalize_scores(entry.get('scores'))
        )
    return deepcopy(history)


def _prepared_inputs(problem, protocol):
    preparation = {}
    states = {}
    for role, expected in (('receptor', PreparedReceptor), ('partner', PreparedLigand)):
        prepared = getattr(problem, role)
        if not isinstance(prepared, expected) and not _is_pdbqt_input(prepared):
            raise ArgumentError(
                arg_name=f'problem.{role}',
                reason='Fixed-pose scoring requires an already prepared object or PDBQT input.',
            )
        assessment = assess_preparation(prepared)
        if (
            assessment['provisional_reasons']
            and not protocol.allow_provisional_preparation
        ):
            raise ArgumentError(
                arg_name=f'problem.{role}',
                reason='Known provisional preparation requires allow_provisional_preparation=True (dockingmt#5).',
            )
        state = getattr(prepared, 'state_id', None)
        declared = problem.metadata.get(f'{role}_state_id')
        if state is not None and declared is not None and state != declared:
            raise ArgumentError(
                arg_name=f'problem.{role}',
                reason='Prepared and problem state identifiers disagree.',
            )
        states[role] = state if state is not None else declared
        preparation[role] = {
            'mode': 'provided',
            'state_id': states[role],
            'metadata': deepcopy(getattr(prepared, 'metadata', None)),
            'assessment_report': assessment,
        }
    return preparation, states


def _input_pose(partner, content, states, pose):
    # Explicitly discard the torsion tree only in this geometry projection.
    # The original bytes (including torsions and types) go unchanged to Vina.
    try:
        native = msm.convert(
            'pdbqt_text:' + content.decode('utf-8'),
            to_form='molsysmt.MolSys',
            discard_torsion_tree=True,
        )
        coordinates = msm.get(native, element='atom', coordinates=True)
        xyz = np.asarray(puw.get_value(coordinates, to_unit='angstrom'), dtype=float)
        names = list(msm.get(native, element='atom', name=True))
        elements = list(msm.get(native, element='atom', atom_type=True))
    except Exception as exc:
        raise ArgumentError(
            arg_name='problem.partner',
            reason=f'Cannot read prepared geometry through MolSysMT: {exc}',
        ) from exc
    if (
        xyz.ndim != 3
        or xyz.shape[0] != 1
        or xyz.shape[2] != 3
        or not xyz.shape[1]
        or not np.isfinite(xyz).all()
    ):
        raise ArgumentError(
            arg_name='problem.partner',
            reason='Supply one nonempty finite ligand conformation.',
        )
    if pose is None:
        metadata = {'pose_atom_order': 'pdbqt_record_order'}
        stored = coordinates[0]
        if isinstance(partner, PreparedLigand):
            order = partner.pdbqt_atom_indices
            stored = partner.coordinates[order]
            source = (
                partner.source_molsys
                if partner.source_molsys is not None
                else partner.to_molecular_system()
            )
            keys = _molecular_atom_keys(source)
            keys = [keys[index] for index in order]
            if [key['atom_name'] for key in keys] != names or [
                key['element'] for key in keys
            ] != elements:
                raise ArgumentError(
                    arg_name='problem.partner',
                    reason='Prepared ligand identity differs from its rendered PDBQT.',
                )
            metadata = {
                'pose_atom_order': 'verified_pdbqt_order',
                'source_atom_keys': keys,
                'prepared_atom_indices': order,
                'selected_atom_indices': order,
                'selected_partner_n_atoms': partner.n_atoms,
            }
        pose = DockingPose(
            stored,
            partner_state_id=states['partner'],
            receptor_state_id=states['receptor'],
            metadata=metadata,
        )
    for role in ('partner', 'receptor'):
        identity = getattr(pose, f'{role}_state_id')
        if (
            identity is not None
            and states[role] is not None
            and identity != states[role]
        ):
            raise ArgumentError(
                arg_name='pose',
                reason=f'The {role} state does not match the prepared input.',
            )
    target = np.asarray(
        puw.get_value(pose.coordinates, to_unit='angstrom'), dtype=float
    )
    if (
        target.shape != xyz[0].shape
        or not np.isfinite(target).all()
        or not np.allclose(target, xyz[0], rtol=0, atol=GEOMETRY_TOLERANCE_ANGSTROM)
    ):
        raise ArgumentError(
            arg_name='pose',
            reason='Pose coordinates must match the prepared ligand in PDBQT record order.',
        )
    identity_check = 'positional_only'
    if pose.metadata.get('source_atom_keys') is not None:
        keys = pose._verified_atom_keys()
        if [key['element'] for key in keys] != elements or any(
            key.get('atom_name') is not None and key['atom_name'] != name
            for key, name in zip(keys, names)
        ):
            raise ArgumentError(
                arg_name='pose',
                reason='Pose atom names or elements differ from the prepared input.',
            )
        identity_check = 'names_and_elements'
    return pose, {
        'atom_order': 'pdbqt_record_order',
        'identity_check': identity_check,
        'coordinate_tolerance': {
            'value': GEOMETRY_TOLERANCE_ANGSTROM,
            'unit': 'angstrom',
        },
        'state_checks': {
            role: 'matched'
            if states[role] is not None
            and getattr(pose, f'{role}_state_id') is not None
            else 'unknown'
            for role in ('partner', 'receptor')
        },
    }


def score_prepared(backend, problem, protocol, pose, score_name):
    protocol = VinaProtocol() if protocol is None else protocol
    if not isinstance(protocol, VinaProtocol):
        raise ArgumentError(
            arg_name='protocol', reason='Vina scoring requires a VinaProtocol.'
        )
    timings = _VinaTimings() if protocol.collect_timings else None
    backend.validate_capabilities(protocol)
    _validate_vina_intent(problem, protocol.name)
    if protocol.active_torsion_bonds:
        raise ArgumentError(
            arg_name='protocol.active_torsion_bonds',
            reason='Prepare the ligand torsion tree before fixed-pose scoring.',
        )
    protocol.validate_problem(problem)
    preparation, states = _prepared_inputs(problem, protocol)
    names = [score_name] + [f'{score_name}.{component}' for component in COMPONENTS[1:]]
    history = []
    if pose is not None:
        # Validate all prior evidence and name collisions before native setup.
        pose.with_scores(dict.fromkeys(names, 0.0))
        history = _history(pose)
    center, size = _vina_box(problem.search_domain)
    if timings is not None:
        timings.end_phase('validation')
    temp_files = []
    result = None
    try:
        staged = backend._stage_inputs(
            problem.receptor, problem.partner, protocol, temp_files
        )
        input_pose, geometry = _input_pose(
            problem.partner, staged['partner_pdbqt'], states, pose
        )
        if timings is not None:
            timings.end_phase('input_projection')
        import vina

        engine = vina.Vina(
            sf_name=protocol.scoring,
            cpu=protocol.cpu,
            seed=protocol.seed if protocol.seed is not None else 0,
            verbosity=0,
        )
        engine.set_receptor(rigid_pdbqt_filename=staged['receptor_file'])
        if staged['partner_file'] is not None:
            engine.set_ligand_from_file(staged['partner_file'])
        else:
            engine.set_ligand_from_string(staged['partner_string'])
        if timings is not None:
            timings.end_phase('engine_setup')
        engine.compute_vina_maps(center=center, box_size=size)
        if timings is not None:
            timings.end_phase('affinity_maps')
        values = np.asarray(engine.score())
        if values.shape != (8,):
            raise ArgumentError(
                arg_name='scores',
                reason='Vina.score() must return exactly eight components.',
            )
        scores = _normalize_scores(dict(zip(names, values)))
        if timings is not None:
            timings.end_phase('native_scoring')
        info = engine.info()
        version = getattr(vina, '__version__', 'unknown')
        context = {
            'stage': 'scoring',
            'receptor_sha256': staged['artifacts']['receptor']['sha256'],
            'partner_sha256': staged['artifacts']['partner']['sha256'],
            'backend_box': {'center': center, 'size': size, 'unit': 'angstrom'},
            'weights': [float(weight) for weight in info['weights']],
            'grid_spacing': {'value': float(info['box_spacing']), 'unit': 'angstrom'},
            'preparation_assessment': {
                role: preparation[role]['assessment_report']['assessment']
                for role in preparation
            },
        }
        definitions = {
            name: {
                'schema_version': '1.0',
                'method': f'AutoDock Vina/{protocol.scoring}',
                'method_version': version,
                'component': component,
                'kind': 'empirical',
                'unit': 'kcal/mol',
                'preferred_direction': 'lower' if component == 'total' else None,
                'context': context,
            }
            for name, component in zip(names, COMPONENTS)
        }
        result = input_pose.with_scores(scores, score_definitions=definitions)
        evaluation = {
            'schema_version': '1.0',
            'operation': 'score',
            'backend': backend.name,
            'backend_version': version,
            'dockingmt_version': __version__,
            'molsysmt_version': msm.__version__,
            'protocol': protocol.to_dict(),
            'applied_parameters': {
                'scoring': protocol.scoring,
                'cpu': protocol.cpu,
                'seed': info['seed'],
                'allow_provisional_preparation': protocol.allow_provisional_preparation,
                'capture_backend_inputs': protocol.capture_backend_inputs,
                'collect_timings': protocol.collect_timings,
            },
            'unused_search_parameters': ['exhaustiveness', 'n_poses', 'energy_range'],
            'seed_role': 'engine initialization only; no stochastic search',
            'backend_artifacts': staged['artifacts'],
            'geometry_check': geometry,
            'preparation': preparation,
            'scores': scores,
            'score_definitions': result.score_definitions,
        }
        # Record only the scores created by this evaluation, not earlier stages.
        evaluation['score_definitions'] = {
            name: evaluation['score_definitions'][name] for name in names
        }
        result.metadata['scoring_history'] = history + [deepcopy(evaluation)]
        if timings is not None:
            timings.end_phase('result_normalization')
        return result
    finally:
        _cleanup_staged_files(temp_files)
        if timings is not None and result is not None:
            timings.end_phase('cleanup')
            report = timings.to_dict()
            report['scope'] = (
                'VinaBackend.score body; excludes public decorators and export'
            )
            result.metadata['scoring_history'][-1]['timings'] = report
